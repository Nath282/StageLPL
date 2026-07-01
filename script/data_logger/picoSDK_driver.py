#!/Users/nathanleretif/StageLPL/script/data_logger/pyenv/bin/python3

# --------- PACKAGE IMPORT ---------
import ctypes
from datetime import datetime
from picosdk.usbtc08 import usbtc08 as tc08
from picosdk.errors import PicoError
# ----------------------------------

class TC08device :

    def __init__(self, ENABLED_CHANNELS, THERMOCOUPLE_TYPES, mains_rejections_mode, buffer_length, logger):
        # Attributes setting
        self.ENABLED_CHANNELS = ENABLED_CHANNELS
        self.THERMOCOUPLE_TYPES = THERMOCOUPLE_TYPES
        self._mains_rejections_mode = mains_rejections_mode
        self._buffer_length = buffer_length
        self.logger = logger

        # Initialisation
        self.THERMOCOUPLE_TYPES[0] = ord(' ')
        self.chandle = None
        self.temp_buffer = (ctypes.c_float * buffer_length)() 
        self.times_ms_buffer = (ctypes.c_int32 * buffer_length)() 
        self.overflow = ctypes.c_int16()
        self.chandle = self._open_unit()


    def _open_unit(self) :
        status = tc08.usb_tc08_open_unit()
        if status > 0 : 
            self.logger.debug("Unit opened successfully")
            return status
        else : 
            self.logger.critical("Failed device opening")
            raise PicoError("Failed device opening")
            return None
        
    def _set_mains(self) :
        if self._mains_rejections_mode is not None : 
            status = tc08.usb_tc08_set_mains(self.chandle, self._mains_rejections_mode)
            if status > 0 : 
                self.logger.debug(f"Mains noise rejection set at {self._mains_rejections_mode}")
            else : 
                self.logger.error("Failed mains noise rejection setting")
                raise PicoError("Failed mains noise rejection setting")
        else : 
            self.logger.debug("No mains rejection set")

    def _set_channel(self, channel, thermocouple_type) :
        status = tc08.usb_tc08_set_channel(self.chandle, channel, thermocouple_type)
        if status > 0 : 
            self.logger.debug(f"Channel {channel} setup successful")
        else : 
            self.logger.critical(f"Unsuccessful channel {channel} setup")
            raise PicoError(f"Unsuccessful channel {channel} setup")
        
    def _get_minimum_interval_ms (self) :
        t = tc08.usb_tc08_get_minimum_interval_ms(self.chandle)
        if t > 0 : 
            self.logger.debug(f"minimum time interval set at {t} ms")
            self.minimum_interval_ms = t
        else : 
            self.logger.critical("Unsuccessful minimum interval retrieval")
            raise PicoError("Unsuccessful minimum interval retrieval")
        
    def _run (self) :
        status = tc08.usb_tc08_run(self.chandle, self.minimum_interval_ms)
        if status > 0 : 
            self.logger.debug("Unit successfully running")
        else : 
            self.logger.critical("Could not run the device")
            raise PicoError("Could not run the device")
        
    def connect (self) :
        self._set_mains()
        for chan in (self.ENABLED_CHANNELS + [0]) :
            self._set_channel(chan, self.THERMOCOUPLE_TYPES[chan])
        self._get_minimum_interval_ms()
        self._run()
        self.logger.info("Unit connected and running")

    def get_temp (self, chan) :
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
        status = tc08.usb_tc08_close_unit(self.chandle)
        if status > 0 : 
            self.logger.info("Device closed")
        else :
            self.logger.critical("Unsuccessful device closing")
            raise PicoError("Unsuccessful device closing")

