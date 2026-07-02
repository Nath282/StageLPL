
@echo off
:: ------------------------------------------
:: Automated start for measuring temperatures
:: ------------------------------------------

:: Start of grafana agent
command "grafana pdc agent" /d path/to/pdc/agent /b ./pdc -token "token" -cluster "cluster" -gcloud-hosted-grafana-id "jsp"

timeout /T 5

:: Start of influxDB
command "influxdb" /b influxdb3 serve --node-id node0

timeout /T 5

python temp_acquisition.py 