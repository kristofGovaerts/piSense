"""
this code senses motion, and activates LEDs & provides environment stats when activated.
"""

import adafruit_dht
import RPi.GPIO as GPIO
import time
from sensors.sense import sense_temp_hum, sense_motion
from tools.reporting import *
from tools.time import current_time, is_active, timestr_to_delta

# globals
ACTIVITY_NUM = 5  # number of activations to cache, minimum amount to caclulate frequency from
ACTIVITY_THRESH = 15  # frequency threshold in activations per minute.
ACTIVITY_STOP = 5  # max inactive time allowed in seconds before the activity flag is turned off again.

# define pins
PIR_PIN = 23  # motion detector
DHT11_PIN = 17  # temp/hum
GREEN_PIN = 26  # green led
RED_PIN = 16  # red led

# initialize sensors
sensor = adafruit_dht.DHT11(DHT11_PIN)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.output(GREEN_PIN, False)  # turn off
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.output(RED_PIN, False)

# initialize reporting
save_report()  # initialize file
lastN = [None] * ACTIVITY_NUM  # initialize
last_motion = timestr_to_delta(current_time())
active = False

while True:
    # TODO: try sensing less often
    # TODO: always turn off LEDs after script
    if sense_motion(PIR_PIN):
        h, t = sense_temp_hum(sensor, wait=0)
        ts = current_time()  # timestamp as str
        last_motion = timestr_to_delta(ts)

        d = lastN.pop(0)  # remove oldest timestamp
        lastN.append(ts)

        # red LED flickers for 1s for each motion. Green pin activates if is_active, otherwise it shuts down.
        GPIO.output(RED_PIN, True)
        output = """Timestamp: {} --- Temperature: {}, humidity: {}, is_active: {}""".format(ts, t, h, active)
        if is_active(lastN, t=ACTIVITY_NUM, f=ACTIVITY_THRESH):
            # here we want to start filming until is_active becomes false.
            if not active:
                # this means it's the start of the active period
                send_alert('test', output)
            GPIO.output(GREEN_PIN, True)
            active = True
        else:
            # here we want to take a picture and send
            GPIO.output(GREEN_PIN, False)
            active = False


        print(output)
        add_line([ts, t, h, active])
        time.sleep(0.5)
        GPIO.output(RED_PIN, False)

    delta = timestr_to_delta(current_time()) - last_motion
    if delta.total_seconds() > ACTIVITY_STOP:
        GPIO.output(GREEN_PIN, False)
        active = False

    time.sleep(1)
