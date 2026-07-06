
@echo off
:: ------------------------------------------

:: Automated start for measuring temperatures

:: ------------------------------------------

:: Se placer dans le dossier du script

cd /d "%~dp0"

:: Kill InfluxDB and Grafana Agent if they are running

taskkill /IM influxdb3.exe /F >nul 2>&1

taskkill /IM grafana-agent.exe /F >nul 2>&1

:: Start Grafana PDC Agent

start "" /B cmd /c ^

    "cd /d C:\path\to\pdc\agent && pdc.exe -token token -cluster cluster -gcloud-hosted-grafana-id jsp"

timeout /T 5 /NOBREAK >nul

:: Start InfluxDB

start "" /B influxdb3 serve --node-id node0

timeout /T 5 /NOBREAK >nul

:: Start main program

python main.py