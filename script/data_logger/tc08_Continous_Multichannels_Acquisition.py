#!/Users/nathanleretif/StageLPL/script/data_logger/pyenv/bin/python3

# --------- PACKAGE IMPORT ---------
from time import time, sleep
from datetime import datetime
from picoSDK_driver import TC08device
from influxdb_client_3 import InfluxDBClient3, Point

import logging
logging.basicConfig(
    level=logging.DEBUG,  # Niveau de base (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Format du message
    filename = 'temp_acquisition.log',  # Fichier de sortie (ou None pour console)
    filemode='a'  # 'w' pour écraser à chaque exécution, 'a' pour ajouter
)
# ----------------------------------


# --------- CONFIGURATION ----------
# Data Logger
ENABLED_CHANNELS = [1, 2]               # Defines which channels to enable (1-8). 0 is the Cold Junction.
THERMOCOUPLE_TYPES = {k : ord('K') for k in range(1,9)}
MAIN_REJECTION_MODE = 0                 # used to set mains noise rejection : 0 for 50Hz (UE) ; 1 for 60Hz (North America)
BUFFER_LENGTH = 1                       # set the buffer length for the temperature measurement, must be at least one
#Time between measures (due to the script execution time, actual time between two measurement may be higher)
waiting_time = 1                      
# InfluxDB3
HOST = 'http://localhost:8181'
DATABASE = 'tempDB'
TOKEN = 'apiv3_UUsS01-Qi8t0Dik_DSF29fFHDsoimFz60TWP5wzs0iOGJFTI8Yinh5qlZH9srijsBsAubNc27Eo0ziNTqppz2A'
# ----------------------------------


# --------- CORE PROGRAM ----------

# Create the client for data logger TC08
device = TC08device(ENABLED_CHANNELS, 
                    THERMOCOUPLE_TYPES, 
                    MAIN_REJECTION_MODE, 
                    BUFFER_LENGTH, 
                    logger=logging)

# Create InlfuxDB client
client = InfluxDBClient3(host=HOST,
                            database=DATABASE,
                            token=TOKEN)

try:
    
    device.connect()
    print("Device running, type Ctrl C to stop")

    while True : 

        points = []

        for chan in device.ENABLED_CHANNELS : 
            temp = device.get_temp(chan)
            if temp is not None :
                points.append(Point("temperatures").tag("channel",chan).field("temp",temp).time(datetime.now()))

        if len(points) > 0 : 
            client.write(points, DATABASE)
            logging.debug("Export of previous points to influxDB client successful")

        sleep(waiting_time) # influxdb client writing time ensure minimum delay between two loop even if waiting_time=0 (otherwise set it at status["min_interval_ms"]/1000 s)

except KeyboardInterrupt : 
    logging.info("Requested stop of the program")
    print("")
    print("Requested program stop")

finally : 
    # Close Data Logger Unit
    device.close()
    print("Device closed")
    # Close InfluxDB client
    client.close()
# ---------------------------------


"""
terminal command to print the influxdb database : 
influxdb3 query --database tempDB --token apiv3_UUsS01-Qi8t0Dik_DSF29fFHDsoimFz60TWP5wzs0iOGJFTI8Yinh5qlZH9srijsBsAubNc27Eo0ziNTqppz2A 'SELECT * FROM temperatures'
"""