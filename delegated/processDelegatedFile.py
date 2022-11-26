import os
import logging
import sys
import pandas as pd

if len(sys.argv) < 2:
    print('usage: ', sys.argv[0], ' delegated_file.txt [year month]')
    sys.exit()

# Logging 
FORMAT = '%(asctime)s %(processName)s %(message)s'
logging.basicConfig(
        format=FORMAT, filename='country-hege.log' , 
        level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S'
        )
logging.info(f'Started: {sys.argv}')

countries = []
if len(sys.argv) > 3:
    year = sys.argv[2]
    month = sys.argv[3]


delegated_file = sys.argv[1]
output_directory = delegated_file+'_results/'
os.makedirs(output_directory, exist_ok=True)

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
    os.system(f'python3 bin/country-hege -t 10000 -w file {filename_in} > {filename_out}_ASweights.txt')
    os.system(f'python3 bin/country-hege -t 10000 -w file -r {filename_in} > {filename_out}_ASweights_onlyTransit.txt')
    os.system(f'python3 bin/country-hege -t 10000 -m 0.01 {cc} > {filename_out}_eyeballWeights.txt')
    os.system(f'python3 bin/country-hege -t 10000 -m 0.01 -r {cc} > {filename_out}_eyeballWeights_onlyTransit.txt')


