# country-as-hegemony: Measuring AS dependency of a country

## Installation
Requirement: https://github.com/InternetHealthReport/abondance

## Example

To get the AS dependencies of Japan, run the following command:
```
$ python3 country-hege.py JP
Found 159 eyeball networks in JP
2914, 0.13931283386237597, +
2516, 0.1361312235573578, +
17676, 0.12757191920492195, +
4713, 0.0781475736286703, +
6939, 0.07497293092232676, -
3257, 0.052850402040864816, -
9605, 0.043622171840001125, +
2497, 0.042800560588185994, +
3356, 0.03921785318903309, -
9824, 0.027111878146210522, +
```
The '+' represent eyeball networks, the '-' are transit networks. These results are biasied towards big eyeballs networks. 
The -r option remove eyeballs networks from the AS hegemony computation.

```
$ python3 country-hege.py JP -r
Found 159 eyeball networks in JP
2914, 0.30166805522874185, +
6939, 0.1627171223971076, -
3257, 0.11470360344494396, -
3356, 0.08511626981907577, -
2497, 0.07474038259844215, +
2516, 0.05601388161450471, +
1299, 0.0472417860536261, -
9824, 0.024108171008297943, +
17676, 0.024046031306026786, +
3491, 0.02102740458813737, -
```



## References
This is a follow up of the work done at APRICOT19 Hackathon: https://github.com/munhyunsu/APRICOT19
AS Hegemony: https://ihr.iijlab.net/ihr/hegemony/
