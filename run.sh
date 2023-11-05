echo 'Starting Country AS Hegemony..' \
&& cd /app \
&& rm -rf data/ihr/delegated-extended* \
&& echo 'removed data/ihr/delegated-extended*' \
&& rm -rf cache \
&& echo 'removed cache' \
&& wget https://www.nro.net/wp-content/uploads/apnic-uploads/delegated-extended -P data/ihr/ \
&& echo 'Downloaded delegated-extended from apinic uploads' \
&& python3 delegated/processDelegatedFile.py data/ihr/delegated-extended \
&& echo 'Finished processing delegated-extended dir' \
&& python3 delegated/push2kafka.py data/ihr/delegated-extended_results/ \
&& echo 'Pushed processing results to Kafka' \
&& echo 'Finished Country AS Hegemony'