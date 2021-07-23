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


def take_photo(name=None):
    if name is None:
        name = current_time() + '.jpg'
    print("Taking a photo...")
    camera.start_preview()
    time.sleep(5)
    camera.capture(name)
    camera.stop_preview()

if __name__ == '__main__':
    print("Recording for five secs...")
    camera_start(name='test.h264')
    camera_stop()
