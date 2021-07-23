from picamera import PiCamera
import time
from tools.time import current_time

camera = PiCamera()


def camera_start(name=None):
    if name is None:
        name = current_time()
    camera.start_preview()
    camera.start_recording(name + '.h264')


def camera_stop():
    camera.stop_recording()
    camera.stop_preview()