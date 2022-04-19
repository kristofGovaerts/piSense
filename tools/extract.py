import imutils
import glob
import numpy as np
import cv2
from tools.convert import *
from tools.time import timestr_to_delta
import matplotlib
matplotlib.use('Agg')  # turn off visualisation or matplotlib.pyplot doesn't work
import matplotlib.pyplot as plt
import datetime


def mask_area(mask, thresh=1):
    m = np.copy(mask)
    m[mask < thresh] = 0
    m[mask >= thresh] = 1
    return np.count_nonzero(mask)


def extract_subject(im, bg, thresh=0.05, mode='rgb', output_size=(128, 128), pad=200, buf=10,
                    min_vol = 100.0, max_vol = 10000.0, return_area=True):
    """
    Extracts the subject from an rgb image and associated background.
    :param im: An image.
    :param bg: A background.
    :param thresh: A threshold value between 1 and 0. How different should pixels be?
    :param mode: 'rgb' or 'gray', determines whether output is rgb or gray.
    :param output_size: The size of the output image. Will be square.
    :param pad: How many pixels to pad the image with. Should be larger if using larger images.
    :param buf: The amount of extra pixels to take
    :param min_vol: The minimum allowed contour volume. If detected subject is smaller, consider this noise.
    :param max_vol: The maximum allowed contour volume. If detected subject is larger, consider this an outlier.
    :param return_area: Whether the area of the subject contour should also be returned.
    :return: A 2D (if mode = 'gray') or 3D (if mode = 'rgb') array with x/y dims equal to output_size.
    """
    img = cv2.imread(im)
    bgn = cv2.imread(bg)

    imgr = imutils.resize(img, width=bgn.shape[1])
    d = np.abs(bgr2gray(imgr).astype('float')/255-bgr2gray(bgn).astype('float')/255)
    db = cv2.GaussianBlur(d, (21,21), 0)
    db[db < thresh] = 0
    db[db >= thresh] = 1
    contours, hierarchy = cv2.findContours(db.astype('uint8'), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    try:
        largest_contour = contours[np.argmax([len(c) for c in contours])]
        area = cv2.contourArea(largest_contour)

        x, y, w, h = cv2.boundingRect(largest_contour)
        cp = (int(round(x+w/2)), int(round(y+h/2)))  # center point
        x = int(round(cp[0] - max(w, h)/2))
        y = int(round(cp[1] - max(w, h)/2))
        w, h = (max(w, h), max(w, h))

        x, y, w, h = resize_rectangle(x, y, w, h, imgr.shape, img.shape)
        yl0 = y+pad-buf
        yl = yl0+h+buf
        xl0 = x+pad-buf
        xl = xl0+w+buf

        out = np.zeros((img.shape[0]+(2*pad), img.shape[1]+(2*pad), 3))
        out = out.astype('uint8')
        out[pad:-pad, pad:-pad, :] = img

        if yl - yl0 == 0 or xl - xl0 == 0 or w * h < 50*50 or w * h > 500*500:
            print("No output.")
            out = None
            area = None

        elif min_vol > area or area > max_vol:
            print("Subject size not within allowed min/max values.")
            out = None
            area = None
        else:
            out = out[yl0:yl, xl0:xl, :]
            out = cv2.resize(out, dsize=output_size)
            if mode == 'gray':
                out = bgr2gray(im)
    except ValueError:
        print("No subject found.")
        out = None
        area = None
    if return_area:
        out = (out, area)
    return out


def get_images_and_backgrounds(ext='.jpg', folder='', date=datetime.date.today()):
    """
    Gets a list of all normal images and all images with the suffix '_BG'.

    :param ext: The image extension. Default = .jpg.
    :param folder: The folder name. Default is current working dir.
    :param date: The date. If not None, filters only for that date.
    :return: A list of image filenames, and background filenames.
    """
    l = glob.glob(folder + '*' + ext)
    l = [i for i in l if '_D.jpg' not in i and 'mosaic' not in i]
    bgs = [i for i in l if '_BG.jpg' in i]
    ims = [i for i in l if '_BG.jpg' not in i]
    if date is not None:
        ims = [i for i in ims if
             timestr_to_delta(i.replace('_', ':').split('.')[0]).date() == date]
    return ims, bgs


def get_background_for_im(im, bgs):
    """
    Finds the best (most recent) background for an image.
    :param im: An image filename.
    :param bgs: A list of background filenames.
    :return: A background filename from bgs.
    """
    imt = im.split('.')[0].replace('_', ':')
    imtd = timestr_to_delta(imt)
    bg_times = [timestr_to_delta(bg.split('_BG.')[0].replace('_', ':')) for bg in bgs
                if (imtd - timestr_to_delta(bg.split('_BG.')[0].replace('_', ':'))).total_seconds() >= 0]
    bg = str(np.max(bg_times)).replace(':', '_') + '_BG.jpg'
    return bg
