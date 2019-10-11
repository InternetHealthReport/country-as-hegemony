# country-as-hegemony: Measuring AS dependency of a country

## Installation

pip install country-as-hegemony


## Example

To get the AS dependencies of Japan, run the following command:
```
$ python3 country-hege.py JP
# Found 166 eyeball networks in JP on 2019-09-29T00:00:00+00:00
2914, 0.27661613861709505, +
2516, 0.25968996183607757, +
17676, 0.1974546945536009, +
4713, 0.15525111414563947, +
1299, 0.13595634758208053, -
9605, 0.10072894639780244, +
174, 0.08765424779438354, -
2497, 0.06338680212620768, +
9824, 0.05253467345731747, +
2527, 0.03509657300628496, +
```
The '+' represent eyeball networks, the '-' are transit networks. These results are biasied towards big eyeballs networks. 
The -r option remove eyeballs networks from the AS hegemony computation.

```
$ python3 country-hege.py JP -r
# Found 166 eyeball networks in JP on 2019-09-29T00:00:00+00:00
2914, 0.27580372217582483, +
1299, 0.13595634758208053, -
174, 0.08765424779438354, -
2516, 0.05994903574329003, +
2497, 0.04637372262121612, +
3356, 0.027235210986714956, -
9824, 0.021176697891166645, +
3491, 0.0191735214924131, -
2519, 0.01604299099396895, +
3257, 0.01316708668625293, -
```



## References
This is a follow up of the work done at APRICOT19 Hackathon: https://github.com/munhyunsu/APRICOT19
AS Hegemony: https://ihr.iijlab.net/ihr/hegemony/
