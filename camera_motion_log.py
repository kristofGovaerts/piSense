"""
this code senses motion using only the camera, and generates a log.
"""

import adafruit_dht
import time
import numpy as np
from sensors.sense import sense_temp_hum
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

