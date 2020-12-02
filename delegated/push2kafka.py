import sys
import glob
import msgpack
import logging
import arrow
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic

MIN_HEGE = 0.0001

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        logging.error('Message delivery failed: {}'.format(err))
    else:
        # print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))
        pass


def parse_res_line(line):
    words = line.split(',')

    asn = int(words[0])
    hege = float(words[1])
    try:
        orig_weight = float(words[2])
    except ValueError:
        orig_weight = 0.0

    return asn, hege, orig_weight


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('usage: ', sys.argv[0], 'resultsDirectory/')
        sys.exit()

    # Logging 
    FORMAT = '%(asctime)s %(processName)s %(message)s'
    logging.basicConfig(
            format=FORMAT, filename='ihr-kafka-country-hege.log' , 
            level=logging.WARN, datefmt='%Y-%m-%d %H:%M:%S'
            )
    logging.info("Started: %s" % sys.argv)
    logging.info("Arguments: %s" % sys.argv)


    # Create kafka topic
    topic = 'ihr_hegemony_countries_ipv4'
    admin_client = AdminClient({'bootstrap.servers':'kafka1:9092, kafka2:9092, kafka3:9092'})

    topic_list = [NewTopic(topic, num_partitions=3, replication_factor=2)]
    created_topic = admin_client.create_topics(topic_list)
    for topic, f in created_topic.items():
        try:
            f.result()  # The result itself is None
            logging.warning("Topic {} created".format(topic))
        except Exception as e:
            logging.warning("Failed to create topic {}: {}".format(topic, e))

    # Create producer
    producer = Producer({'bootstrap.servers': 'kafka1:9092,kafka2:9092,kafka3:9092',
        # 'linger.ms': 1000, 
        'default.topic.config': {'compression.codec': 'snappy'}}) 

    working_directory = sys.argv[1]

    for fullname in glob.glob(working_directory+'/*_dependencies_*.txt'):
        fname = fullname.rpartition('/')[2]

        words = fname.replace('.txt','').split('_')
        cc, _, weight = words[:3]
        transit = False
        if 'onlyTransit' in fname:
            transit = True

        with open(fullname, 'r') as fin:
            header = True
            timestamp = None
            for line in fin:
                if header:
                    # still in the file header
                    if line.startswith('# Results for '):
                        timestamp = arrow.get(line.rpartition(' ')[2]).timestamp
                        header = False
                    continue

                # append results to output
                weight_str = 'eyeball'
                if weight == 'ASweights':
                    weight_str = 'AS'

                asn, hege, orig_weight = parse_res_line(line)

                # output_line = f'{cc}, {weight_str}, {transit}, {line}'
                # fout.write(output_line)
                result = {'ts': timestamp, 'cc': cc, 'weight': weight_str, 
                        'transit_only': transit, 'asn':asn, 'hege': hege, 
                        'original_weight': orig_weight}
                logging.debug('going to produce something')
                producer.produce(
                        topic, 
                        msgpack.packb(result, use_bin_type=True), 
                        callback=delivery_report,
                        timestamp = timestamp*1000
                        )

                logging.debug('produced something')
                # Trigger any available delivery report callbacks from previous produce() calls
                producer.poll(0)

    # Wait for any outstanding messages to be delivered and delivery report
    # callbacks to be triggered.
    producer.flush()

