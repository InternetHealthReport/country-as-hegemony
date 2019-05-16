import requests
import argparse
from ihr.hegemony import Hegemony
from collections import defaultdict

def get_pop_estimate(cc):
    url = 'http://v6data.data.labs.apnic.net/ipv6-measurement/Economies/{cc}/{cc}.asns.json'.format(cc=cc)

    params = dict(
        m=0.001
    )

    resp = requests.get(url=url, params=params)
    pop_est = resp.json() # Check the JSON Response Content documentation below
    return {x['as']:x for x in pop_est}

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('country_code', type=str,
                    help='Country code')
    parser.add_argument('-e', '--eyeball', action='count',
                        help='count eyeball asn')
    parser.add_argument('-n', '--noweight', action='count',
                        help="don't weight by eyeball population")
    parser.add_argument('-t', '--top', type=int, default=10,
                        help="print top ASN")
    args = parser.parse_args()

    pop_est = get_pop_estimate(args.country_code)
    print('Found {} eyeball networks in {}'.format(len(pop_est), args.country_code))

    hege = Hegemony(originasns=pop_est.keys(), start="2019-05-15 00:00", end="2019-05-15 00:01")
    results = defaultdict(float)
    weight_sum = 0

    for hege_all_asn in hege.get_results():
        for hege in hege_all_asn:

            w = hege['hege']
            asn = hege['asn']
            originasn = hege['originasn']

            # don't count originasn (eyeball network)
            if not args.eyeball and asn==originasn:
                continue

            if not args.noweight:
                w  *= pop_est[originasn]['percent']

            results[asn] += w
            weight_sum += w

    results = {asn:w/weight_sum for asn, w in results.items()}
    sorted_results = sorted(results.items(), key=lambda kv: kv[1])
    for i in range(1,min(len(sorted_results),args.top+1)):
        print(sorted_results[len(sorted_results)-i])

