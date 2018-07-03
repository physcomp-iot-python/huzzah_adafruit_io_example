import board
import digitalio
import machine
import time
from analogio import AnalogIn

import adafruit_io

# Network 'Hotspot' settings
ESSID    = 'nasa'
PASSWORD = 'mars-adventure'

#-Adafruit IO settings
USER_NAME = "donblair" #PLEASE CHANGE TO YOUR AIO USERNAME
AIO_KEY = '3515b3ecee734780927d7f4ab1654917'  #PLEASE CHANGE TO YOUR AIO KEY

# create one adafruit_io.Feed object per sensor, configure once during
# instantiation, and use to post values many times.
# Each sensor's' feed should have a unique name!

ANALOG_FEED_NAME = 'analog-feed-test-number-1' #PLEASE CHANGE TO YOUR AIO FEED NAME
analog_feed = adafruit_io.Feed(user_name = USER_NAME,
                               key = AIO_KEY,
                               feed_name = ANALOG_FEED_NAME,
                               )

# some utility functions
def get_adc():
    with AnalogIn(board.ADC) as ai:
        return ai.value/65535.0
    
def blink(sleeptime):
    import machine
    led = machine.Pin(0,machine.Pin.OUT)
    led.value(0)
    time.sleep(sleeptime)
    led.value(1)

def do_connect(essid=ESSID,password=PASSWORD):
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(essid, password)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

################################################################################
# Main
################################################################################
do_connect() #connect to network

while True:
    try:
        adc_value = get_adc()
        analog_feed.post(adc_value)
        blink(2.0)
    except Exception as exc:
        print("Caught: {}".format(repr(exc)))

