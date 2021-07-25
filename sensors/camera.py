from picamera import PiCamera
import picamera.array
import time
from tools.time import current_time
import cv2
import numpy as np
import matplotlib

matplotlib.use('Agg')  # turn off visualisation or matplotlib.pyplot doesn't work
import matplotlib.pyplot as plt

camera = PiCamera()


def get_frame(bw=False):
    """Gets a single frame from the camera and returns it as an array.
    If bw == True, this frame is converted to grayscale."""
    with picamera.array.PiRGBArray(camera) as output:
        camera.resolution = (1280, 780)
        camera.capture(output, 'rgb')
        out = output.array
    if bw:
        out = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY)
    return out


def take_photo(name=None):
    """
    Takes a single photo and saves to 'name'.
    """
    if name is None:
        name = current_time() + '.jpg'
    print("Taking a photo...")
    camera.start_preview()
    time.sleep(1)
    camera.capture(name)
    camera.stop_preview()


def compare_frames(f1, f2, input='rgb', thresh=20, blur=(21, 21)):
    """
    Compares two frames and returns a delta value corresponding to the
    fraction of pixels that are different by a factor of more than thresh.
    :param f1: First image. XxYxC RGB or XxY grayscale image.
    :param f2: Second image. XxYxC RGB or XxY grayscale image.
    :param input: 'rgb' if input is rgb. Otherwise f1 and f2 should be grayscale.
    :param thresh: A threshold value. The factor by which pixels have to be different.
    :param blur: Motion blur denoising factor.
    :return: A delta value corresponding to the
    fraction of pixels that are different by a factor of more than thresh.
    """
    if input == 'rgb':
        g1 = cv2.cvtColor(f1, cv2.COLOR_RGB2GRAY)
        g2 = cv2.cvtColor(f2, cv2.COLOR_RGB2GRAY)
    else:
        g1 = f1
        g2 = f2

    g1 = cv2.GaussianBlur(np.array(g1).astype('float32'), blur, 0)
    g2 = cv2.GaussianBlur(np.array(g2).astype('float32'), blur, 0)

    delta = np.abs(g1-g2)
    frac_different = len(delta[delta>thresh]) / np.prod(delta.shape)
    return frac_different


def compare_with_cache(f1, cache, input='rgb', thresh=20):
    """
    Compares an image with a series of image.
    :param f1: First image. XxYxC RGB or XxY grayscale image.
    :param cache: A list of images.
    :param input: 'rgb' if RGB. Otherwise should provide grayscale imgs.
    :param thresh: A threshold value.
    :return: A delta value corresponding to the
    fraction of pixels that are different by a factor of more than thresh,
    averaged over all images in cache.
    """
    deltas = [compare_frames(f1, f, input=input, thresh=thresh) for f in cache]
    mean_frac = np.mean(deltas)
    return mean_frac


def write_difference_figure(bg, im, dest):
    """
    Writes a figure showing the difference between two frames to dest.
    :param bg: First RGB image, probably the background.
    :param im: Second RGB image.
    :param dest: Where to save.
    :return: Nothing.
    """
    bg = np.array(cv2.cvtColor(bg, cv2.COLOR_RGB2GRAY)).astype('float32')
    im = np.array(cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)).astype('float32')
    d = np.abs(bg-im)

    d_ratio = d.shape[0]/d.shape[1]
    fig = plt.figure(figsize=(5, 5))
    plt.imshow(d, vmin=0, vmax=100)
    plt.colorbar(orientation='horizontal')
    plt.tight_layout()
    fig.savefig(dest)
    plt.close(fig)

