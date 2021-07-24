"""
this code senses motion using only the camera, and generates a log.
"""

import adafruit_dht
import time
import numpy as np
import imutils
import cv2
from sensors.sense import sense_temp_hum
from tools.reporting import *
from tools.time import current_time, is_active, timestr_to_delta
from sensors.camera import get_frame, compare_with_cache

# globals
CACHE_NUM = 3  # number of activations to cache, minimum amount to calculate activity from
DELTA_THRESH = 0.01
FRAMERATE_REST = 1.0/5.0
FRAMERATE_ACTIVE = 1.0

# define pins
DHT11_PIN = 17  # temp/hum

# initialize sensors
sensor = adafruit_dht.DHT11(DHT11_PIN)

# initialize reporting
save_report()  # initialize file
active = False
current_name = current_time()
frame_buf = [imutils.resize(get_frame(), width=500) for i in range(CACHE_NUM)]
bg = frame_buf[0]

while True:
    current_name = current_time()
    f = get_frame()
    f_small = imutils.resize(f, width=500)
    d = compare_with_cache(f_small, frame_buf)
    if d > DELTA_THRESH:
        h, t = sense_temp_hum(sensor, wait=0)
        output = """Timestamp: {} --- Temperature: {}, humidity: {}, is_active: {}"""
        add_line([current_name, t, h, active])
        print("Activity detected! {}".format(np.round(d, 3)))
        print(output.format(current_name, t, h, active))
        cv2.imwrite(current_name + '.png', f)
        if not active:
            cv2.imwrite(current_name + '.png', bg)
            send_alert(current_name + '.png', output.format(current_name, t, h, active))
        active = True
    else:
        print("No activity. {}".format(np.round(d, 3)))
        bg = frame_buf[0] # we only want to update bg if there is no activity
        active = False

    frame_buf = frame_buf[1:] + [f_small]

    if active:
        time.sleep(1/FRAMERATE_ACTIVE)
    else:
        time.sleep(1/FRAMERATE_REST)

