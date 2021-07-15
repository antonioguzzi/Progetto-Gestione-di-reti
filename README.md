# Forecasting the server status using single/double exponential smoothing
## introduzione
Il progetto ha come obbiettivo la creazione di uno script in python in grado di prevedere lo stato di un server attraverso l'utlizzo di single & double exponential smoothing e l'analisi di risposte http: tramite prometheus si invia la query ***probe_http_duration_seconds*** al server, catturando la risposta di quest'ultimo è possibile analizzare la duranta della richiesta http per ogni sua fase (connect, processing, resolve, tls, transfer). **IMPORTANTE: per l'utilizzo della query *probe_http_duration_seconds* è necessaria la configurazione e l'utilizzo della [blackbox](https://github.com/prometheus/blackbox_exporter)**
## Prerequisiti e Esecuzione
Per poter utilizzare il programma è necessario eseguire i comandi

`pip3 install requests` 

`pip3 install matplotlib`

Per poi eseguire il programma con il comdando

`python3 main.py`

L'applicazione permette di fare analisi su dati prelevati direttamente da Prometheus. Per l'analisi di un server è necessario utilizzare una BlackBox e Prometheus che sono scaricabili direttamente dal sito ufficiale di Prometheus: https://prometheus.io/download/
Dopo aver scaricato la versione adeguata al proprio sistema, devono essere copiati i file che sono contenuti nella cartella prometheus della repository, nelle cartelle blackbox e prometheus scaricate.
A questo punto possiamo lanciare prima la blackbox e successivamente promtheus e quest'ultimo permettera di effettuare query al link: http://localhost:9090/.
