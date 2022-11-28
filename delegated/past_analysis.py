import os

YEARS = [2019]
MONTHS = range(1,13,1)
DAYS = range(1,7,1)

for year in YEARS:
    for month in MONTHS:
        for day in DAYS:
            delegated_file = f'{year}_{month:02d}_{day:02d}_combined-stat'
            output_directory = delegated_file+'_results/'

            os.system(f'python delegated/processDelegatedFile.py {year} {month} {day}')
            os.system(f'python delegated/push2kafka.py {output_directory} ihr_hegemony_countries_ipv4_past &')

