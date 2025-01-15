#!/bin/bash

years=('2019' '2020')
months=('01' '02' '03' '04' '05' '06' '07' '08' '09' '10' '11' '12')
months2019=('10' '11' '12')
months2020=('01' '02' '03' '04' '05' '06' '07' '08' '09' '10' '11' '12')
days=('15')

for y in "${years[@]}" ; do
  months=$months2019

  if [ "$y" == "2020" ] 
  then months=$months2020
  fi

  for m in "${months[@]}" ; do
    for d in "${days[@]}" ; do

      date="$y$m$d"

      echo "Analyzing data for $y/$m/$d"
      mkdir -p data/ihr/$date/;
      wget "https://ftp.ripe.net/pub/stats/ripencc/nro-stats/$date/combined-stat" -P "data/ihr/$date/" ;
      python3 delegated/processDelegatedFile.py "data/ihr/$date/combined-stat";
      python3 delegated/push2kafka.py "data/ihr/$date/combined-stat_results/"

    done
  done
done

