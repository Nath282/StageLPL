#!/Users/nathanleretif/StageLPL/script/data_logger/pyenv/bin/python3
# author : Nathan Le Rétif, initially based on https://github.com/picotech/picosdk-python-wrappers/blob/master/usbtc08Examples/tc08StreamingModeMultiChExample.py example

"""
Python files collecting temperatures data through the PicoTech TC-08 data logger and export it to a InfluxDB database
Set to run continously until Keyboard Interrupt (Ctrl C)
"""

# --------- PACKAGE IMPORT ---------
from time import sleep
from datetime import datetime, timezone
from TC08_driver import TC08device
from influxdb_client_3 import InfluxDBClient3, Point
import logging
# ----------------------------------


# --------- CONFIGURATION ----------
# Data Logger
ENABLED_CHANNELS = [1, 2]                                   # Defines which channels to enable (1-8)
THERMOCOUPLE_TYPES = {chan : 'K'                            # Dictionnary of all thermocouple types (default K) 
                      for chan in ENABLED_CHANNELS}         
MAIN_REJECTION_MODE = 0                                     # used to set mains noise rejection : 0 for 50Hz (UE) ; 1 for 60Hz (North America) ; None to disable

# Interval between measures (s)
WAITING_TIME = 1                                            # Time between measurement of all channels (due to the script execution time, add ~1s to the actual time)

# InfluxDB3
HOST = 'http://localhost:8181'                              # HTTP address of the port influxDB is listening to 
DATABASE = 'tempDB'                                         # Name of the influxDB database
TOKEN = 'apiv3_h548YCVAVkjDrOgfgCXOVx4mo73XZVk_dQKbAQQL87VNjD2xeOe0WvZZgtXqfmuUK5mN_vwuegQNMpPjWdjDLQ' # InfluxDB admin token

# Logging 
LOG_FILENAME = 'temp.acquisition.log'                       # log filename, set to None for logs in console
LOG_LEVEL = logging.DEBUG                                   # log level, set the minimum level for which logs are stored (DEBUG, INFO, WARNING, ERROR, CRITICAL) -> set to DEBUG for debugging and INFO otherwise
LOG_FILEMODE = 'a'                                          # set to 'a' for logs to be added at each execution, set to 'w' for scratching
# ----------------------------------


# --------- CORE PROGRAM -----------

# Logs configuration
logging.basicConfig(               
    level = LOG_LEVEL,  
    format = '%(asctime)s - %(levelname)s - %(message)s',  
    filename = LOG_FILENAME,  
    filemode = LOG_FILEMODE )

# Create clients for data logger and influxDB
device = TC08device(logger = logging)
client = InfluxDBClient3(host=HOST,
                         database=DATABASE,
                         token=TOKEN)

try:

    # Connection to data logger
    device.connect(ENABLED_CHANNELS, THERMOCOUPLE_TYPES, MAIN_REJECTION_MODE)
    print("Device running, input Ctrl C to stop")

    # Main loop for data acquisition
    while True : 

        points = []

        # Temperature Measurements
        for chan in ENABLED_CHANNELS : 
            temp = device.get_temp(chan)
            if temp is not None :
                points.append(Point("temperatures").tag("channel",chan).field("temp",temp).time(datetime.now(timezone.utc)))

        # Writing into InfluxDB database
        if len(points) > 0 : 
            client.write(points, DATABASE)
            logging.debug("Export of previous points to influxDB client successful")

        # Waiting time before the next measure
        sleep(WAITING_TIME) 

# Encapsulation of KeyboardInterrupt errors to stop the program
except KeyboardInterrupt : 
    logging.info("Requested stop of the program")
    print("\nRequested program stop")

# Encapsulates unwanted errors and add the Traceback in the logs
except Exception : 
    logging.exception("Stop of a program due to an unexpected error")

# Close client and device after the program stops
finally : 
    client.close()
    device.close()
    print("Device closed")




