"""
this code senses motion using only the camera, assuming the motion sensor was activated once,, and generates a log.
"""

import RPi.GPIO as GPIO
import adafruit_dht
import time, os
import numpy as np
import imutils
import cv2
from sensors.sense import sense_temp_hum, sense_motion
from tools.reporting import *
from tools.time import current_time, timestr_to_delta
from sensors.camera import get_frame, compare_with_cache, write_difference_figure, compare_frames

# globals
CACHE_NUM = 3  # number of activations to cache, minimum amount to calculate activity from
DELTA_THRESH = 0.01  # lower threshold - minimum num of pixels that have to change
DELTA_THRESH2 = 0.6  # upper thresh - because if this is very high we've moved the camera!
ALERT_INTERVAL = 120
BG_INTERVAL = 120

print("Initalizing sensors...")
# define pins
DHT11_PIN = 17  # temp/hum
PIR_PIN = 23  # motion detector

# initialize sensors
sensor = adafruit_dht.DHT11(DHT11_PIN)
GPIO.setup(PIR_PIN, GPIO.IN)

# initialize reporting
if not os.path.exists('log.csv'):
    save_report()  # initialize file
recording = False
active = False
current_name = current_time()
frame_buf = [imutils.resize(get_frame(), width=500) for i in range(CACHE_NUM)]
bg = frame_buf[0]
last_alert = None
last_capture = None
last_motion = None

print("Start recording at {}".format(current_name))
while True:
    if sense_motion(PIR_PIN):
        recording = True
        print("Recording...")
    if recording:
        current_name = current_time()
        last_motion = timestr_to_delta(current_name)
        f = get_frame()
        f_small = imutils.resize(f, width=500)
        if not active:
            d = compare_frames(f_small, bg)
        else:
            d = compare_with_cache(f_small, frame_buf)
        if DELTA_THRESH < d < DELTA_THRESH2:
            h, t = sense_temp_hum(sensor, wait=0)
            output = """Timestamp: {} --- Temperature: {}, humidity: {}, is_active: {}"""
            add_line([current_name, t, h, active])
            print("Activity detected! {}".format(np.round(d, 3)))
            print(output.format(current_name, t, h, active))
            cv2.imwrite(current_name + '.jpg', f)
            write_difference_figure(bg, f_small, current_name + '_D.jpg')
            if not active:
                cv2.imwrite(current_name + '_BG.jpg', bg)
                di = np.abs(np.array(cv2.cvtColor(bg, cv2.COLOR_RGB2GRAY)).astype('float32')
                            - np.array(cv2.cvtColor(f_small, cv2.COLOR_RGB2GRAY)).astype('float32'))
                if last_alert is None:
                    send_alert(current_name + '.jpg', output.format(current_name, t, h, active))
                    last_alert = timestr_to_delta(current_name)
                elif last_alert is not None and (timestr_to_delta(current_name) -
                                                 last_alert).total_seconds() > ALERT_INTERVAL:
                    send_alert(current_name + '.jpg', output.format(current_name, t, h, active))
                    last_alert = timestr_to_delta(current_name)
                else:
                    print("Last alert was recent. Not sending.")
            active = True
        else:
            if active:  # end of active period
                print("Stop active recording. Rebuilding cache.")
                bg = frame_buf[-1]  # we only want to update bg if there is no activity
                frame_buf = [imutils.resize(get_frame(), width=500) for i in range(CACHE_NUM)]
            else:
                bg = frame_buf[0]  # we only want to update bg if there is no activity
            active = False
            recording = False
            print("Stop recording.")

        frame_buf = frame_buf[1:] + [f_small]
    else:
        if not active and (last_capture is None or (timestr_to_delta(current_time()) -
                                                    last_capture).total_seconds() > BG_INTERVAL):
            print("Refreshing background.")
            last_capture = timestr_to_delta(current_time())
            f = get_frame()
            f_small = imutils.resize(f, width=500)
            bg = f_small
            frame_buf = frame_buf[1:] + [f_small]
    time.sleep(1)