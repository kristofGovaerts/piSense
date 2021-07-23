from picamera import PiCamera
import time
from tools.time import current_time

camera = PiCamera()


def camera_start(name=None):
    if name is None:
        name = current_time()  + '.h264'
    camera.start_preview()
    camera.start_recording(name)


def camera_stop():
    camera.stop_recording()
    camera.stop_preview()
