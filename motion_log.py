"""
this code senses motion, and activates LEDs & provides environment stats when activated.
"""

import adafruit_dht
import RPi.GPIO as GPIO
import time
from sensors.sense import sense_temp_hum, sense_motion
from tools.reporting import *
from tools.time import current_time, is_active, timestr_to_delta

PIR_PIN = 23  # motion detector
DHT11_PIN = 17  # temp/hum
GREEN_PIN = 26  # green led
RED_PIN = 16  # red led

# initialize sensors
sensor = adafruit_dht.DHT11(DHT11_PIN)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(RED_PIN, GPIO.OUT)

# initialize reporting
save_report()  # initialize file
last20 = [None] * 20  # initialize
last_motion = current_time()
active = False

while True:
    # TODO: try sensing less often
    if sense_motion(PIR_PIN):
        h, t = sense_temp_hum(sensor, wait=0)
        ts = current_time()  # timestamp as str
        last_motion = timestr_to_delta(ts)

        d = last20.pop(0)  # remove oldest imestamp
        last20.append(ts)

        # red LED flickers for 1s for each motion. Green pin activates if is_active, otherwise it shuts down.
        GPIO.output(RED_PIN, True)
        if is_active(last20):
            GPIO.output(GREEN_PIN, True)
            active = True
        else:
            GPIO.output(GREEN_PIN, False)
            active = False

        print("""Timestamp: {} --- Temperature: {}, humidity: {}, is_active: {}""".format(ts, t, h, active))
        add_line([ts, t, h, active])
        time.sleep(1)
        GPIO.output(RED_PIN, False)

    delta = timestr_to_delta(current_time()) - last_motion
    if delta.total_seconds() > 20:
        GPIO.output(GREEN_PIN, False)
        active = False

    time.sleep(1)
