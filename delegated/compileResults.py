import sys
import glob

if len(sys.argv) < 2:
    print('usage: ', sys.argv[0], 'resultsDirectory/')
    sys.exit()

working_directory = sys.argv[1]
fout = open(f"{working_directory}/all_results.csv", 'w')

fout.write('#  country code, weighting scheme, only transit?, ASN, AS Hegemony, weight\n')

for fullname in glob.glob(working_directory+'/*_dependencies_*.txt'):
    fname = fullname.rpartition('/')[2]
    print(fname)

    words = fname.replace('.txt','').split('_')
    cc, _, weight = words[:3]
    transit = False
    if len(words) > 3:
        transit = True

    with open(fullname, 'r') as fin:
        header = True
        for line in fin:
            if header:
                # still in the file header
                if line.startswith('# Results for '):
                    header = False
                continue

            # append results to output
            weight_str = 'eyeball'
            if weight == 'ASweights':
                weight_str = 'AS'

            output_line = f'{cc}, {weight_str}, {transit}, {line}'
            fout.write(output_line)

