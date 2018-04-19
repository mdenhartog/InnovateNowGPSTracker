# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# pylint: disable=E0401,E1101,W0703,C0411,C0103,E1205
#

"""
InnovateNow Outdoor Tracker program
"""

import machine
import config
import pycom
import gc
import sys
import time

from network import LoRa
from pytrack import Pytrack
from pycoproc import WAKE_REASON_ACCELEROMETER

from version import VERSION
from inmsg import GPSMessage, EnvironMessage
from ingps import GPS
from inlora import LORAWAN
from inenvsensor import Environment
from LIS2HH12 import LIS2HH12

# Initialize logging
import inlogging as logging
try:
    logging.basicConfig(level=config.LOG_LEVEL, stream=sys.stdout)
except ImportError:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

log = logging.getLogger(__name__)

lora = None

def start_network():
    """ Start network logic """
    # TODO: SigFox, WLAN and BLE
    
    log.debug('Start networking ...')
    global lora
    if config.LORA_ENABLED:
        log.info('Start LoRa network')        
        if not lora:
            if config.LORA_ACTIVATION == LoRa.OTAA:
                log.debug('Start LoRa OTAA')
                lora = LORAWAN(app_eui=config.LORA_APP_EUI, app_key= config.LORA_APP_KEY)

            if config.LORA_ACTIVATION == LoRa.ABP:
                log.debug('Start LoRa ABP')
                lora = LORAWAN(activation=LoRa.ABP, dev_addr=config.LORA_DEV_ADDR, 
                               nwk_swkey=config.LORA_NWK_SWKEY, app_swkey=config.LORA_APP_SWKEY)

            lora.start() # Start joining LoRa Network                   

# Stop default heartbeat
pycom.heartbeat(False)

# Led orange
pycom.rgbled(config.LED_COLOR_WARNING)

log.info('Start InnovateNow Outdoor Tracker version {}', VERSION)
log.debug('Memory allocated: ' + str(gc.mem_alloc()) + ' ,free: ' + str(gc.mem_free()))

# Set watchdog 5min
wdt = machine.WDT(timeout=300000)

try:
    
    # Init pytrack board
    py = Pytrack()

    wdt.feed() # Feed

    # Start network
    start_network()

    wdt.feed() # Feed
        
    # Init gps
    gps = GPS(i2c=py.i2c)

    # Init environmental sensor
    environ = Environment(i2c=py.i2c)

    # Led off
    pycom.heartbeat(False)

    wdt.feed() # Feed

    # Read GPS coordinates
    # Retry counter is used to stop when there is no GPS signal available
    time.sleep(15) # Give GPS time to find a fix
    retry_counter = 0
    while not gps.coords_valid and retry_counter < 5:
        gps.update()
        retry_counter += 1
        time.sleep(5)  # Give the GPS time to get a fix

    wdt.feed() # Feed
    
    log.debug('Prepare GPS messsage')
    gps_msg = GPSMessage(latitude=gps.latitude[0],
                         longitude=gps.longitude[0],
                         altitude=gps.altitude,
                         speed=gps.speed(),
                         course=gps.course,
                         direction=gps.direction)

    log.debug('Prepare Environmental messsage')
    env_msg = EnvironMessage()
    if config.ENVIRONMENT_SENSOR_AVAILABLE:
        if environ.temperature and environ.humidity and environ.barometric_pressure:
            env_msg = EnvironMessage(temperature=environ.temperature,
                                    humidity=environ.humidity,
                                    barometric_pressure=environ.barometric_pressure)
        else:
            log.error('Problem with environmental sensor')                            

    # Send message
    pycom.rgbled(config.LED_COLOR_OK)

    msg = gps_msg.lora() + '|' + env_msg.lora() + '|{0:.1f}'.format(py.read_battery_voltage())
    
    # Awake from Accelerometer
    if py.get_wake_reason() == WAKE_REASON_ACCELEROMETER:
        msg += '|1' # Means awake from Accellerometer
    
    log.debug ('LoRa message to send {}', msg)
    lora.send_str(message=msg)
    pycom.heartbeat(False)

    # Awake on Accelerometer
    if config.DEEPSLEEP_AWAKE_ON_ACCELEROMETER:
        
        # Disable wakeup source from INT pin
        py.setup_int_pin_wake_up(False)

        # Enable activity and also inactivity interrupts, using the default callback handler
        py.setup_int_wake_up(True, True)

        acc = LIS2HH12()
                
        # enable the activity/inactivity interrupts
        # set the accelereation threshold to 2000mG (2G) and the min duration to 200ms
        acc.enable_activity_interrupt(config.ACCELEROMETER_THRESHOLD, 
                                      config.ACCLEROMETER_DURATION_MS)

    # Go to sleep
    if config.DEEPSLEEP_ENABLED:
        log.info('Start sleeping for {} seconds', config.DEEPSLEEP_IN_SECONDS)
        time.sleep(2) # So everything can finish

        # Sleep
        py.setup_sleep(config.DEEPSLEEP_IN_SECONDS)
        py.go_to_sleep()    

except Exception as e:
    pycom.rgbled(config.LED_COLOR_ERROR)
    log.error('Unexpected error {}', e)

    time.sleep(5) # Wait for 5secs before reset
    machine.reset() # Reset device
