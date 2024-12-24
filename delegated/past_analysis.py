import os

YEARS = [2019,2020]
MONTHS = range(1,13,1)
DAYS = range(1,8,1)

for year in YEARS:
    for month in MONTHS:
        for day in DAYS:
            delegated_file = f'{year}_{month:02d}_{day:02d}_combined-stat'
            output_directory = 'data/past/'+delegated_file+'_results/'

            #os.system(f'python3 delegated/processDelegatedFile.py {year} {month} {day}')
            os.system(f'python3 delegated/push2kafka.py {output_directory} ihr_hegemony_countries_ipv4_20192020 {year}/{month:02d}/{day:02d}')

