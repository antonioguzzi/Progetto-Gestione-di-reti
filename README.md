# Forecasting the server status using single/double exponential smoothing
## introduzione
Il progetto ha come obbiettivo la creazione di uno script in python in grado di prevedere lo stato di un server attraverso l'utlizzo di single & double exponential smoothing e l'analisi di risposte http: tramite prometheus si invia la query ***probe_http_duration_seconds*** al server, catturando la risposta di quest'ultimo è possibile analizzare la duranta della richiesta http per ogni sua fase (connect, processing, resolve, tls, transfer). **IMPORTANTE: per l'utilizzo della query *probe_http_duration_seconds* è necessaria la configurazione e l'utilizzo della [blackbox](https://github.com/prometheus/blackbox_exporter)**
## Prerequisiti
Per poter utilizzare il programma è necessario eseguire i comandi

`pip3 install requests` 

`pip3 install matplotlib`

