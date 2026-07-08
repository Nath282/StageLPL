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
import argparse
# ----------------------------------

# ------ ARGUMENT PARSING ----------
# add flags to be passed to the python file when executed through a terminal to be able to change key parameters without modifying the python file itself
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--waitingtime", type=float, default=10, help="time between meausures")
parser.add_argument("--loglevel", choices=["DEBUG","INFO","WARNING","ERROR","CRITICAL"], default="INFO", help="defines the level of logging (DEBUG, INFO, WARNING, ERROR, CRITICAL) -> set to DEBUG for debugging and INFO otherwise") 
parser.add_argument("--logfilename", type=str, default="temp_acquisition.log", help="log filename, set to None for logs in console")
parser.add_argument("--logfilemode", choices=['a','w'], default='a', help="set to 'a' for logs to be added at each execution, set to 'w' for scratching")
args = parser.parse_args()
# ----------------------------------

# --------- CONFIGURATION ----------
# Data Logger
ENABLED_CHANNELS = [1, 2, 3]                                # Defines which channels to enable (1-8)
THERMOCOUPLE_TYPES = {chan : 'K'                            # Dictionnary of all thermocouple types (default K) 
                      for chan in ENABLED_CHANNELS}     
CHANNEL_LABELS = {1 : "TOP",
                  2 : "DOWN",
                  3 : "LEFT"}   
MAIN_REJECTION_MODE = 0                                     # used to set mains noise rejection : 0 for 50Hz (UE) ; 1 for 60Hz (North America) ; None to disable

# Interval between measures (s)
WAITING_TIME = args.waitingtime                             # Time between measurement of all channels (due to the script execution time, add ~1s to the actual time)

# InfluxDB3
HOST = 'http://localhost:8181'                              # HTTP address of the port influxDB is listening to 
DATABASE = 'tempDB'                                         # Name of the influxDB database
TOKEN = 'apiv3_h548YCVAVkjDrOgfgCXOVx4mo73XZVk_dQKbAQQL87VNjD2xeOe0WvZZgtXqfmuUK5mN_vwuegQNMpPjWdjDLQ' # InfluxDB admin token
# ----------------------------------


# --------- CORE PROGRAM -----------

# Logs configuration
logging.basicConfig(               
    level = getattr(logging, args.loglevel),  
    format = '%(asctime)s - %(levelname)s - %(message)s',  
    filename = args.logfilename,  
    filemode = args.logfilemode )

# Create clients for data logger and influxDB
device = TC08device(logger = logging)
print("Device opened")
client = InfluxDBClient3(host=HOST,
                         database=DATABASE,
                         token=TOKEN)

try:

    # Connection to data logger
    device.connect(ENABLED_CHANNELS, THERMOCOUPLE_TYPES, MAIN_REJECTION_MODE)
    print(f"Device running, {WAITING_TIME}s between measurements  \ninput Ctrl C to stop")

    # Main loop for data acquisition
    while True : 

        points = []

        # Temperature Measurements
        for chan in ENABLED_CHANNELS : 
            temp = device.get_temp(chan)
            if temp is not None :
                points.append(Point("temperatures").tag("channel",chan).tag("label",CHANNEL_LABELS[chan]).field("temp",temp).time(datetime.now(timezone.utc)))

        # Writing into InfluxDB database
        if len(points) > 0 : 
            client.write(points, DATABASE)
            logging.debug("Export of previous points to influxDB client successful")

        # Waiting time before the next measure
        sleep(WAITING_TIME) 

# Encapsulation of KeyboardInterrupt errors to stop the program
except KeyboardInterrupt : 
    logging.info("Requested stop of the program")
    print("Requested program stop")

# Encapsulates unwanted errors and add the Traceback in the logs
except Exception : 
    logging.exception("Stop of a program due to an unexpected error")
    print("Stop of a program due to an unexpected error")

# Close client and device after the program stops
finally : 
    client.close()
    device.close()
    print("Device closed \nTo restart the program, type python main.py in the current terminal \nwaiting time and log settings can be modified with appropriate flags directly in the terminal, type python main.py --help for more information")




