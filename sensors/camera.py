from picamera import PiCamera
import picamera.array
import time
from tools.time import current_time
import cv2
import numpy as np

camera = PiCamera()


def get_frame(bw=False):
    with picamera.array.PiRGBArray(camera) as output:
        camera.resolution = (1280, 720)
        camera.capture(output, 'rgb')
        out = output.array
        print('Captured %dx%d image' % (
                output.array.shape[1], output.array.shape[0]))
    if bw:
        out = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY)
    return out


def take_photo(name=None, exposure=1.0):
    if name is None:
        name = current_time() + '.jpg'
    print("Taking a photo...")
    camera.start_preview()
    time.sleep(exposure)
    camera.capture(name)
    camera.stop_preview()


def compare_frames(f1, f2, input='rgb', thresh=20):
    if input == 'rgb':
        g1 = cv2.cvtColor(f1, cv2.COLOR_RGB2GRAY)
        g2 = cv2.cvtColor(f2, cv2.COLOR_RGB2GRAY)
    else:
        g1 = f1
        g2 = f2

    g1 = np.array(g1).astype('float32')
    g2 = np.array(g2).astype('float32')

    delta = np.abs(g1-g2)
    frac_different = len(delta[delta>thresh]) / np.prod(delta.shape)
    return frac_different
