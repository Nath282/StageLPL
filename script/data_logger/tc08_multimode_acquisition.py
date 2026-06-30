#!/Users/nathanleretif/StageLPL/script/data_logger/pyenv/bin/python3

# --------- PACKAGE IMPORT ---------
import ctypes
from time import time, sleep
from datetime import datetime
from picosdk.usbtc08 import usbtc08 as tc08
from picosdk.errors import PicoSDKCtypesError
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
NUM_SAMPLES = 10
ENABLED_CHANNELS = [1, 2] # Defines which channels to enable (1-8). 0 is the Cold Junction.
waiting_time = 2 # set the delay between two measures, due to the script execution time, actual time between two measurement may be higher
THERMOCOUPLE_TYPE = ord('K') # defines the type of thermocouple : Use 32 (ASCII space) to disable.
mains_rejection_mode = 0 # used to set mains noise rejection : 0 for 50Hz (UE) ; 1 for 60Hz (North America)
buffer_length = 1 # set the buffer length for the temperature measurement, must be at least one
# InfluxDB3
HOST = 'http://localhost:8181'
DATABASE = 'tempDB'
TOKEN = 'apiv3_UUsS01-Qi8t0Dik_DSF29fFHDsoimFz60TWP5wzs0iOGJFTI8Yinh5qlZH9srijsBsAubNc27Eo0ziNTqppz2A'
# ----------------------------------



# --------- PRELIMINARY FUNCTIONS ----------
def assert_status_ok (status) : 
    # Function checking for TC-08 API calls error 
    if status > 0 : errorCheck = True
    else : errorCheck = False
    return errorCheck

def data_logger_setup (status, chandle, ENABLED_CHANNELS, THERMOCOUPLE_TYPE, mains_rejection_mode) : 
    # Activate filter for mains noise rejection (aka suppresion du bruit de secteur) 
    status["set_mains"] = tc08.usb_tc08_set_mains(chandle, mains_rejection_mode)
    if not assert_status_ok(status["set_mains"]) :
        logging.error("Unsuccessful API call set_mains")
        raise PicoSDKCtypesError("Unsuccessful API call set_mains")
    # Setup Channels
    status["set_chan_0"] = tc08.usb_tc08_set_channel(chandle, 0, ord(' ')) # Always set channel 0 (Cold Junction)
    for chan in ENABLED_CHANNELS:
        status[f"set_chan_{chan}"] = tc08.usb_tc08_set_channel(chandle, chan, THERMOCOUPLE_TYPE)
        if not assert_status_ok(status[f"set_chan_{chan}"]) :
            logging.critical(f"Unsuccessful channel {chan} setup")
            raise ConnectionError(f"Unsuccessful channel {chan} setup")
    # Get the minimum sampling interval 
    status["min_interval_ms"] = tc08.usb_tc08_get_minimum_interval_ms(chandle) # this determines how fast the device can switch between enabled channels
    if not assert_status_ok(status["min_interval_ms"]) : 
        logging.error("Unsuccessful API call get_minimum_interval_ms")
        raise PicoSDKCtypesError("Unsuccessful API call get_minimum_interval_ms")
    # set tc-08 running
    status["run"] = tc08.usb_tc08_run(chandle, status["min_interval_ms"])
    if not assert_status_ok(status["run"]) :
        logging.critical("Could not run the unit")
        raise ConnectionError("Could not run the unit")
    # Buffer initialization (required by the measurement method)
    temp_buffer = (ctypes.c_float * buffer_length)() 
    times_ms_buffer = (ctypes.c_int32 * buffer_length)() 
    overflow = ctypes.c_int16()
    return temp_buffer, times_ms_buffer, overflow
# ------------------------------------------



# --------- CORE PROGRAM ----------
if __name__ == '__main__' :

    # Create status dictionary to track API calls
    status = {}

    # Open Data Logger Unit
    status["open_unit"] = tc08.usb_tc08_open_unit()
    if not assert_status_ok(status["open_unit"]) : 
        logging.critical("Unsuccessful start of unit")
        raise ConnectionError("Unsuccessful start of unit")
    logging.info("Device started")
    chandle = status["open_unit"]

    # Create InlfuxDB client
    client = InfluxDBClient3(host=HOST,
                             database=DATABASE,
                             token=TOKEN)
    
    try:
        # data logger setup
        temp_buffer, times_ms_buffer, overflow = data_logger_setup(status, chandle, ENABLED_CHANNELS, THERMOCOUPLE_TYPE, mains_rejection_mode)
        logging.info(f"Device running, starting capture of {NUM_SAMPLES} samples over channels {ENABLED_CHANNELS}")

        # data collection
        for sample_id in range(NUM_SAMPLES+1) : 

            points = []
            for chan in ENABLED_CHANNELS : 

                get_temp_return = tc08.usb_tc08_get_temp(
                    chandle, 
                    ctypes.byref(temp_buffer), 
                    ctypes.byref(times_ms_buffer), 
                    len(temp_buffer),
                    ctypes.byref(overflow), # Chanel over range flag
                    chan, # channel
                    0, # units (0 = Centigrade)
                    1  # fill_missing samples
                )

                status["get_temp_return"] = get_temp_return
                if sample_id > 0 :
                    if not assert_status_ok(status["get_temp_return"]) :
                        logging.warning(f"Measurement {sample_id} of channel {chan} failed")
                    else : 
                        points.append(Point("temperatures").tag("channel",chan).field("temp",temp_buffer[0]).time(datetime.now()))

            client.write(points, DATABASE)

            sleep(waiting_time) # influxdb client writing time ensure minimum delay between two loop even if waiting_time=0 (otherwise set it at status["min_interval_ms"]/1000 s)

        logging.info(f"Capture complete")

    finally : 
        # Close Data Logger Unit
        status["close_unit"] = tc08.usb_tc08_close_unit(chandle)
        if not assert_status_ok(status["close_unit"]) : 
            logging.critical("Unsuccessful unit closing")
            logging.debug(f"status : {status}")
            raise ConnectionError("Unsuccessful unit closing")
        logging.debug(f"status : {status}")
        logging.info("Device closed")
        

        # Close InfluxDB client
        client.close()
# ---------------------------------


"""
terminal command to print the influxdb database : 
influxdb3 query --database tempDB --token apiv3_UUsS01-Qi8t0Dik_DSF29fFHDsoimFz60TWP5wzs0iOGJFTI8Yinh5qlZH9srijsBsAubNc27Eo0ziNTqppz2A 'SELECT * FROM temperatures'
"""


        