"""
this code senses motion, and activates LEDs & provides environment stats when activated.
"""

import adafruit_dht
import RPi.GPIO as GPIO
import time
from sensors.sense import sense_temp_hum, sense_motion
from tools.reporting import *
from tools.time import current_time, is_active, timestr_to_delta
from sensors.camera import camera_start, camera_stop, take_photo

# globals
ACTIVITY_NUM = 3  # number of activations to cache, minimum amount to caclulate frequency from
ACTIVITY_THRESH = 15  # frequency threshold in activations per minute.
ACTIVITY_STOP = 3  # max inactive time allowed in seconds before the activity flag is turned off again.
PHOTO_INTERVAL = 60  # one photo each minute

# define pins
PIR_PIN = 23  # motion detector
DHT11_PIN = 17  # temp/hum
# GREEN_PIN = 26  # green led
# RED_PIN = 16  # red led

# initialize sensors
sensor = adafruit_dht.DHT11(DHT11_PIN)
GPIO.setup(PIR_PIN, GPIO.IN)
# GPIO.setup(GREEN_PIN, GPIO.OUT)
# GPIO.output(GREEN_PIN, False)  # turn off
# GPIO.setup(RED_PIN, GPIO.OUT)
# GPIO.output(RED_PIN, False)

# initialize reporting
save_report()  # initialize file
lastN = [None] * ACTIVITY_NUM  # initialize
last_motion = timestr_to_delta(current_time())
active = False
current_name = current_time()
last_photo = timestr_to_delta(current_time())

while True:
    if sense_motion(PIR_PIN):
        h, t = sense_temp_hum(sensor, wait=0)
        ts = current_time()  # timestamp as str
        last_motion = timestr_to_delta(ts)

        d = lastN.pop(0)  # remove oldest timestamp
        lastN.append(ts)

        # red LED flickers for 1s for each motion. Green pin activates if is_active, otherwise it shuts down.
        # GPIO.output(RED_PIN, True)
        output = """Timestamp: {} --- Temperature: {}, humidity: {}, is_active: {}"""
        if is_active(lastN, t=ACTIVITY_NUM, f=ACTIVITY_THRESH):
            # here we want to start filming until is_active becomes false.
            if not active:
                # this means it's the start of the active period. Take a photo and send.
                active = True
                current_name = current_time()
                take_photo(current_name + '.jpg')
                send_alert(current_name + '.jpg', output.format(current_name, t, h, active))
                last_photo = timestr_to_delta(current_name)
            else:
                # just take a photo, don't send an alert.
                current_name = current_time()
                take_photo(current_name + '.jpg')
                last_photo = timestr_to_delta(current_name)
            # GPIO.output(GREEN_PIN, True)
            active = True
        else:
            GPIO.output(GREEN_PIN, False)
            # active = False

        print(output.format(ts, t, h, active))
        add_line([ts, t, h, active])
        time.sleep(0.5)
        # GPIO.output(RED_PIN, False)

    ct = timestr_to_delta(current_time())
    delta = ct - last_motion
    if delta.total_seconds() > ACTIVITY_STOP:
        # GPIO.output(GREEN_PIN, False)
        active = False
        #camera_stop()

    photodelta = ct - last_photo
    if photodelta.total_seconds() > PHOTO_INTERVAL:
        current_name = current_time()
        take_photo(current_name + '_BG.jpg')
        last_photo = ct

    time.sleep(1)
