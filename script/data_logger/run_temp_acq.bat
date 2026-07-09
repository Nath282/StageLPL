
@echo off                                                                   &:: hide all the commands written in the terminal
title Data Logger                                                           &:: specifu the title of the terminal
cd /d "C:\Users\Manip_Bec_Sodium\Documents\People\Nathan"                   &:: Change the working directory

:: INFLUXDB
taskkill /f /Im influxdb3.exe > .\logs\influxdb.log 2>&1                    &:: kill the influxdb process (if it exists), scratch the previous log file and write the new logs and errors
start "" /b ".\influxdb3-core\influxdb3.exe" serve --node-id node0 --data-dir C:\Users\Manip_Bec_Sodium\Documents\People\Nathan\ >> .\logs\influxdb.log 2>&1    &:: launch the InflxDB database in a hidden auxiliary terminal and write logs/error into the given file
echo Launch of InfluDB                                                      &:: print "[...]"

timeout /t 1 /nobreak > nul                                                 &:: wait 1 second 

:: GRFANA PDC
taskkill /f /Im pdc.exe > .\logs\grafana-pdc.log 2>&1                       &:: kill the grafana pdc process (if it exists), scratch the previous log file and write the new logs and errors
start "" /b ".\grafana-pdc\pdc.exe"  -token glc_eyJvIjoiMTgzNjExNSIsIm4iOiJwZGMtbG9mdHlib3h3b29kMjAyNC1kZWZhdWx0LXBkYy01YWM1NGYiLCJrIjoiQk01MDlvNHNoNzQzNloyRVhsbmVLcEk3IiwibSI6eyJyIjoicHJvZC1ldS13ZXN0LTIifX0= -cluster prod-eu-west-2 -gcloud-hosted-grafana-id 1714763 >> .\logs\grafana-pdc.log 2>&1      &:: launch the grafana PDC agent in a hidden auxiliary terminal and write logs/error into the given file
echo Launch of grafana PDC

timeout /t 1 /nobreak > nul                                                 &:: wait 1 second 

:: PYTHON PROGRAM
echo Start of python program
start "Python Data logger" cmd /k "call .\env\Scripts\activate.bat && python main.py"   &:: create an auxiliary terminal, activate the virtual environment and start the python program

echo All process launched, closing this terminal will stop them all
echo To manually control the python program, go to the dedicated terminal
