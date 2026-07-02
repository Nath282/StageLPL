#!/Users/nathanleretif/StageLPL/script/data_logger/pyenv/bin/python3
# author : Nathan Le Rétif

"""
File creating a class TC08device acting as a driver for data logger TC-08 simplifying the actual native driver
-> Greatly simplify uses and increase code clarity + encapsulate errors and logs
Attributes : logger -> logging instance used to print logs 
             chandle -> necessary arguments for all native driver methods except opening, testifying the successful opening of the device (is equal to 1 if success)
             temp_buffer -> buffer in which will be stored the measured temperatures in usb_tc08_get_temp
             times_ms_buffer -> buffer storing the time during temperature measurmment, is not the actual time but a multiple of self.minimum_interval_ms (cf ._get_minimum_interval_ms()), I didn't found any use to it
             overflow -> necessary arguments for temperature measurement, I have no idea why it is that way
More details on the native driver : 
The native driver behavior is strange and rely on C, stored in a compiled file libusbtc08.dylib. When the module is called, it creates an instance of the usbtc08lib class called usbtc08. This object inherits from the Library class which charges the compiled C library. Afterwards, python wrappers are created around the C functions stored in libusbtc08.dylib used to interact with the device, and are associated to the usbtc08 object as methods. These methods are what native python way to interact with the device.
In practice, all methods of usbtc08 returns an integer : 0 for an API call fail and a positive integer in case of a succes (in almost every case this integer is one, except for methods like usb_tc08_get_minimum_interval_ms or usb_tc08_run)
Rmq : at installation, the libusbtc08.dylib was stored in the wrong place in my computer so I had to modify the _load() method in the picosdk.library.py file to explicitely input the absolute path to libusbtc08.dylib for the driver to work
"""

# --------- PACKAGE IMPORT ---------
import ctypes
from datetime import datetime
from picosdk.usbtc08 import usbtc08 as tc08
from picosdk.errors import PicoError
import logging
# ----------------------------------


# --------- CORE PROGRAM -----------
class TC08device :

    def __init__(self, logger : logging, BUFFER_LENGTH=1):
        """
        logger -> logger used to print logs
        BUFFER_LENGTH -> length of the buffers used to measure temperature, I did not found case where it was necessary for it to be more than one 
        """
        self.logger = logger
        self.chandle = self._open_unit()
        self.temp_buffer = (ctypes.c_float * BUFFER_LENGTH)() 
        self.times_ms_buffer = (ctypes.c_int32 * BUFFER_LENGTH)() 
        self.overflow = ctypes.c_int16()
        
    def _open_unit(self) :
        """
        Open the device, this method is used during the initialisation of an instance
        """
        chandle = tc08.usb_tc08_open_unit()
        if chandle > 0 : 
            self.logger.debug("Unit opened successfully")
            return chandle
        else : 
            self.logger.critical("Failed device opening")
            raise PicoError("Failed device opening")
            return None
        
    def _set_mains(self, MAIN_REJECTION_MODE : int) :
        """
        Activate a filter to suppress mains noise (bruit du secteur electrique)
        MAIN_REJECTION_MODE : 0 for 50 Hz (FR,UE,...), 1 for 60Hz (North America)
        """
        status = tc08.usb_tc08_set_mains(self.chandle, MAIN_REJECTION_MODE)
        if status > 0 : 
            self.logger.debug(f"Mains noise rejection mode set at {MAIN_REJECTION_MODE}")
        else : 
            self.logger.error("Failed mains noise rejection setting")
            raise PicoError("Failed mains noise rejection setting")

    def _set_channel(self, channel : int, thermocouple_type : int) :
        """
        Conects to a specific channel (0-8) of the data logger with the relevant thermocouple type 
        CAREFUL : thermocouple_type needs to be the unicode code corresponding to the relevent letter type, use ord() functions to convert a caracter to their unicode code
        """
        status = tc08.usb_tc08_set_channel(self.chandle, channel, thermocouple_type)
        if status > 0 : 
            self.logger.debug(f"Channel {channel} connected successfully")
        else : 
            self.logger.critical(f"Unsuccessful channel {channel} connection")
            raise PicoError(f"Unsuccessful channel {channel} connection")
        
    def _get_minimum_interval_ms (self) :
        """
        checks for the minimul interval between two measurement in the same channel
        """
        t = tc08.usb_tc08_get_minimum_interval_ms(self.chandle)
        if t > 0 : 
            self.logger.debug(f"minimum time interval set at {t} ms")
            self.minimum_interval_ms = t
        else : 
            self.logger.critical("Unsuccessful minimum interval retrieval")
            raise PicoError("Unsuccessful minimum interval retrieval")
        
    def _run (self) :
        """
        Prepare the devide for measurement
        """
        status = tc08.usb_tc08_run(self.chandle, self.minimum_interval_ms)
        if status > 0 : 
            self.logger.debug("Unit successfully running")
        else : 
            self.logger.critical("Could not run the device")
            raise PicoError("Could not run the device")
        
    def connect (self, ENABLED_CHANNELS : list, THERMOCOUPLE_TYPES : dict, MAIN_REJECTION_MODE : int) :
        """
        Secure connection with the device and set all relevant parameters
        Arguments : ENABLED_CHANNELS -> list of channels to enable (1 to 8)
                    THERMOCOUPLE_TYPES -> dictionnary containing the letters corresponfing type of each channel ; ex : {1 : 'K'} for a thermocouple of type K on channel 1)
                    MAIN_REJECTION_MODE -> defines the mode of mains noise rejection (cf _set_mains()), set to None to disable
        Rmq : 
        Thermocouple types are converted to their unicode code in order to work with ._set_channel()
        Cold junction (channel 0 of type ' ') must always be enabled (but I don't know why)
        """
        # Set mains noise filter
        if MAIN_REJECTION_MODE is not None : 
            self._set_mains(MAIN_REJECTION_MODE)
        else : self.logger.debug("No mains rejection set")
        # Enables all channels
        thermocouple_types = {chan : ord(type) for chan,type in THERMOCOUPLE_TYPES.items()}.update({0 : ord(' ')})
        for chan in (ENABLED_CHANNELS + [0]) :
            self._set_channel(chan, thermocouple_types[chan])
        # Device final configuration
        self._get_minimum_interval_ms()
        self._run()
        self.logger.info("Unit connected and running")

    def get_temp (self, chan : int) :
        """
        returns the temperature of the channel chan (0-8)
        """
        status = tc08.usb_tc08_get_temp(self.chandle, 
                                        ctypes.byref(self.temp_buffer), 
                                        ctypes.byref(self.times_ms_buffer), 
                                        len(self.temp_buffer),
                                        ctypes.byref(self.overflow), # Chanel over range flag
                                        chan, # channel
                                        0, # units (0 = Centigrade)
                                        1  # fill_missing samples
                                        )
        if status > 0 : 
            self.logger.debug(f"Measurement of channel {chan} successful, temp = {self.temp_buffer[0]} at {datetime.now()}")
            return self.temp_buffer[0]
        else : 
            self.logger.warning(f"Measurement of channel {chan} failed at {datetime.now()}")
            return None 
        
    def close (self) :
        """
        Close the device
        """
        status = tc08.usb_tc08_close_unit(self.chandle)
        if status > 0 : 
            self.logger.info("Device closed")
        else :
            self.logger.critical("Unsuccessful device closing")
            raise PicoError("Unsuccessful device closing")

