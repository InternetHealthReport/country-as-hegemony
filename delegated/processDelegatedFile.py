import arrow
import os
import logging
import sys
import pandas as pd
import json

URL_DELEGATED = 'https://ftp.ripe.net/ripe/stats/nro-stats/{year}{month:02d}{day:02d}/combined-stat'
URL_HEGE = 'https://ihr-archive.iijlab.net/ihr/hegemony/ipv4/local/{year}/{month:02d}/{day:02d}/ihr_hegemony_ipv4_local_{year}-{month:02d}-{day:02d}.csv.lz4'
FNAME_HEGE = 'ihr_hegemony_ipv4_local_{year}-{month:02d}-{day:02d}.csv.lz4' 
URL_POP = 'https://sg-pub.ripe.net/petros/population_coverage/data_sources/data{day:02d}{month:02d}{year}_0000.json'
FNAME_POP = 'data{day:02d}{month:02d}{year}_0000.json'

if len(sys.argv) < 2:
    print('usage: ', sys.argv[0], ' delegated_file.txt or "year month day"')
    sys.exit()

# Logging 
logging.basicConfig(
    format='%(asctime)s %(processName)s %(message)s',
    level=logging.info,
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler()])
logging.info(f'Started: {sys.argv}')

countries = []
past_delegated = False
delegated_file = sys.argv[1]
date_start = arrow.utcnow().shift(days=-1)
year = date_start.year
month = date_start.month
day = date_start.day

if len(sys.argv) > 3:
    past_delegated = True
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    day = int(sys.argv[3])

    # Dowload delegated file
    os.makedirs('data/past/', exist_ok=True)
    delegated_file = f'data/past/{year}_{month:02d}_{day:02d}_combined-stat'

    # the ripe archive starts from 2019/10/07
    year_r = year
    month_r = month
    day_r = day
    if year < 2019 or ( year == 2019 and month < 11):
        year_r = 2019
        month_r = 10
        day_r = 7
    os.system(f'wget {URL_DELEGATED.format(year=year_r, month=month_r, day=day_r)} -O {delegated_file}')


    # Download population file
    output_directory = delegated_file+'_results/'
    os.makedirs(output_directory, exist_ok=True)
    os.system(f'wget {URL_POP.format(year=year, month=month, day=day)} -P {output_directory}')


output_directory = delegated_file+'_results/'
os.makedirs(output_directory, exist_ok=True)

# Download hegemony values
os.system(f'wget {URL_HEGE.format(year=year, month=month, day=day)} -P {output_directory}')

# Read delegated file
raw_data = pd.read_csv(delegated_file, sep='|', header=None,  
        names=['rir', 'cc', 'type', 'val0', 'val1', 'date', 'status', 'misc0', 'misc1'],
        keep_default_na=False, na_values=[''])

data =  raw_data[raw_data['status']=='assigned']

if not countries:
    countries = data['cc'].unique()
    logging.info(f'Found {len(countries)} countries')

# create AS files per country
for cc in countries:
    asns = data[(data['cc']==cc) & 
            (data['type'] == 'asn')]['val0'].unique()

    filename_in = f'{output_directory}/{cc}_asns.txt'
    filename_out = f'{output_directory}/{cc}_dependencies'

    with open(filename_in, 'w') as fp:
        for asn in asns:
            fp.write(f'{asn} 1\n')

    logging.info(f'Processing {cc}')

    hege_file = f'{output_directory}/{FNAME_HEGE.format(year=year, month=month, day=day)}'
    if past_delegated:

        # Compute past population estimates
        pop_all_file = output_directory+FNAME_POP.format(year=year, month=month, day=day)
        pop_file = f'{output_directory}/{cc}.pop' 

        with open(pop_all_file, 'r') as fp:
            pop_all = json.load(fp)

            with open(pop_file, 'w') as fp_out:
                if not cc in pop_all['countries']:
                    continue

                if not isinstance(pop_all['countries'][cc]['apnic'], list):
                    sys.stderr.write(f'Error: pop is not available for cc={cc}\n')
                    sys.stderr.write(pop_all['countries'][cc]['apnic'])
                    continue

                for asn in pop_all['countries'][cc]['apnic']:
                    if asn['percent'] > 0.01:
                        fp_out.write(f'{asn["as"]} {asn["percent"]}\n')


        os.system(f'python3 bin/country-hege -t 10000 -w file {filename_in} --hege_file {hege_file} > {filename_out}_ASweights.txt')
        os.system(f'python3 bin/country-hege -t 10000 -w file -r {filename_in} --hege_file {hege_file}  > {filename_out}_ASweights_onlyTransit.txt')
        os.system(f'python3 bin/country-hege -t 10000 -w file {pop_file} --hege_file {hege_file}  > {filename_out}_eyeballWeights.txt')
        os.system(f'python3 bin/country-hege -t 10000 -w file -r {pop_file} --hege_file {hege_file}  > {filename_out}_eyeballWeights_onlyTransit.txt')
    else:
        os.system(f'python3 bin/country-hege -t 10000 -w file {filename_in} --hege_file {hege_file}  > {filename_out}_ASweights.txt')
        os.system(f'python3 bin/country-hege -t 10000 -w file -r {filename_in} --hege_file {hege_file}  > {filename_out}_ASweights_onlyTransit.txt')
        os.system(f'python3 bin/country-hege -t 10000 -m 0.01 {cc} --hege_file {hege_file}  > {filename_out}_eyeballWeights.txt')
        os.system(f'python3 bin/country-hege -t 10000 -m 0.01 -r {cc} --hege_file {hege_file}  > {filename_out}_eyeballWeights_onlyTransit.txt')


