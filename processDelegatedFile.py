import os
import sys
import pandas as pd

if len(sys.argv) < 2:
    print('usage: ', sys.argv[0], ' delegated_file.txt')
    sys.exit()

delegated_file = sys.argv[1]
output_directory = delegated_file+'_results/'
os.makedirs(output_directory, exist_ok=True)

data = pd.read_csv(delegated_file, sep='|', header=None, 
        names=['rir', 'cc', 'type', 'val0', 'val1', 'date', 'status'] )

countries = data[data['status']=='allocated']['cc'].unique()
print('Found ', len(countries), ' countries')

# create AS files per country
for cc in countries:
    asns = data[(data['cc']==cc) & 
            (data['status'] == 'allocated') & 
            (data['type'] == 'asn')]['val0'].unique()

    filename_in = f'{output_directory}/{cc}_asns.txt'
    filename_out = f'{output_directory}/{cc}_dependencies'

    with open(filename_in, 'w') as fp:
        for asn in asns:
            fp.write(f'{asn} 1\n')

    print('Processing ', cc)
    os.system(f'python3 bin/country-hege -w file {filename_in} > {filename_out}_ASweights.txt')
    os.system(f'python3 bin/country-hege -w file -r {filename_in} > {filename_out}_ASweights_onlyTransit.txt')
    os.system(f'python3 bin/country-hege -m 0.1 {cc} > {filename_out}_eyeballWeights.txt')
    os.system(f'python3 bin/country-hege -m 0.1 -r {cc} > {filename_out}_eyeballWeights_onlyTransit.txt')


