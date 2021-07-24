"""
this code senses motion using only the camera, and generates a log.
"""

import adafruit_dht
import RPi.GPIO as GPIO
import time
from sensors.sense import sense_temp_hum, sense_motion
from tools.reporting import *
from tools.time import current_time, is_active, timestr_to_delta
from sensors.camera import get_frame, compare_with_cache

# globals
CACHE_NUM = 3  # number of activations to cache, minimum amount to calculate activity from
DELTA_THRESH = 0.01
FRAMERATE = 0.5

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
frame_buf = [get_frame() for i in CACHE_NUM]

while True:
    f = get_frame()
    d = compare_with_cache(f, frame_buf)
    print
    if d < DELTA_THRESH:
        print("Activity detected! {}".format(np.round(d, 3)))
    else:
        print("No activity. {}".format(np.round(d, 3)))

    frame_buf = frame_buf[1:] + f
    time.sleep(1/FRAMERATE)

