"""
this code senses motion using only the camera, and generates a log.
"""

import adafruit_dht
import RPi.GPIO as GPIO
import time
from sensors.sense import sense_temp_hum, sense_motion
from tools.reporting import *
from tools.time import current_time, is_active, timestr_to_delta
from sensors.camera import take_photo, get_frame, compare_frames

# globals
ACTIVITY_NUM = 3  # number of activations to cache, minimum amount to caclulate frequency from
ACTIVITY_THRESH = 15  # frequency threshold in activations per minute.
ACTIVITY_STOP = 3  # max inactive time allowed in seconds before the activity flag is turned off again.
PHOTO_INTERVAL = 60  # one photo each minute

# define pins
DHT11_PIN = 17  # temp/hum

# initialize sensors
sensor = adafruit_dht.DHT11(DHT11_PIN)

# initialize reporting
save_report()  # initialize file
lastN = [None] * ACTIVITY_NUM  # initialize
last_motion = timestr_to_delta(current_time())
active = False
current_name = current_time()
last_photo = timestr_to_delta(current_time())
frame_buf = get_frame()

while True:
    f = get_frame()
    d = compare_frames(frame_buf, f)
    print(d)

    time.sleep(2)

