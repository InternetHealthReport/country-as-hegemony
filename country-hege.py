import requests
import argparse
from ihr.hegemony import Hegemony
from collections import defaultdict
import arrow


def get_pop_estimate(cc, min_population):
    url = 'http://v6data.data.labs.apnic.net/ipv6-measurement/Economies/{cc}/{cc}.asns.json'.format(cc=cc)

    params = dict(
        m=min_population
    )

    resp = requests.get(url=url, params=params)
    pop_est = resp.json() # Check the JSON Response Content documentation below

    return {x['as']:x for x in pop_est}


def compute_hegemony(pop_est, args, date):
    hege = Hegemony(originasns=pop_est.keys(), 
            start=date, end=date.shift(minutes=1))
    results = defaultdict(float)
    originasn_found = set()

    for hege_all_asn in hege.get_results():
        for hege in hege_all_asn:

            w = hege['hege']
            asn = hege['asn']
            originasn = hege['originasn']
            originasn_found.add(hege['originasn'])

            # don't count originasn (eyeball network)
            if args.remove_eyeball and asn==originasn:
                continue

            if not args.noweight:
                w  *= pop_est[originasn]['percent']

            results[asn] += w

    weight_sum = 0
    if args.noweight:
        weight_sum = len(originasn_found)
    else:
        weight_sum = sum([pop_est[oasn]['percent'] for oasn in originasn_found])

    results = {asn:w/weight_sum for asn, w in results.items()}
    return sorted(results.items(), key=lambda kv: kv[1])

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('country_code', type=str,
                        help='Country code')
    parser.add_argument('-r', '--remove_eyeball', action='count',
                        help="don't count origin ASes in hegemony calculation. \
Provides only results for transit networks.")
    parser.add_argument('-n', '--noweight', action='count',
                        help="don't weight by eyeball population")
    parser.add_argument('-t', '--top', type=int, default=10,
                        help="print top ASN")
    parser.add_argument('-m', '--min_population', type=float, default=0.01,
                        help="print top ASN")
    parser.add_argument('-d', '--date', type=str, 
                        help='Fetch data for the given date')
    args = parser.parse_args()

    # set up the date
    date = None
    if args.date is None:
        # Get recent results
        date = arrow.utcnow().shift(days=-2)
    else:
        date = arrow.get(args.date)
    date = date.replace(minute=0, hour=0, second=0, microsecond=0)

    pop_est = get_pop_estimate(args.country_code, args.min_population)
    print('# Found {} eyeball networks in {} on {}'.format(
        len(pop_est), args.country_code, date)
        )

    sorted_results = compute_hegemony(pop_est, args, date)

    for i in range(1,min(len(sorted_results), args.top+1)):
        asn, val = sorted_results[len(sorted_results)-i]
        label = '-'
        if asn in pop_est:
            label = '+'

        print('{}, {}, {}'.format(asn, val, label))

