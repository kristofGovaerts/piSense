import cv2
import imutils
import glob
import numpy as np
from tools.convert import *
from tools.time import timestr_to_delta
import datetime
import matplotlib.pyplot as plt


def extract_subject(im, bg, thresh=0.075, mode='rgb', output_size=(128, 128), pad=200, buf=10):
    """
    Extracts the subject from an rgb image and associated background.
    :param im: An image.
    :param bg: A background.
    :param mode: 'rgb' or 'gray', determines whether output is rgb or gray.
    :param output_size: The size of the output image. Will be square.
    :param buf: The amount of extra pixels to take
    :return:
    """
    img = cv2.imread(im)
    bgn = cv2.imread(bg)

    imgr = imutils.resize(img, width=bgn.shape[1])
    d = np.abs(bgr2gray(imgr).astype('float')/255-bgr2gray(bgn).astype('float')/255)
    db = cv2.GaussianBlur(d, (21,21), 0)
    db[db<thresh] = 0
    db[db>=thresh] = 1
    contours, hierarchy = cv2.findContours(db.astype('uint8'), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    try:
        largest_contour = contours[np.argmax([len(c) for c in contours])]
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

        if yl - yl0 == 0 or xl - xl0 == 0:
            print("No output.")
            out = None
        else:
            out = out[yl0:yl, xl0:xl, :]
            out = cv2.resize(out, dsize=output_size)
            if mode == 'gray':
                out = bgr2gray(im)
    except ValueError:
        print("No subject found.")
        out = None
    return out


def get_images_and_backgrounds(ext='.jpg', folder='', date=None):
    l = glob.glob(folder + '*' + ext)
    l = [i for i in l if '_D.jpg' not in i]
    bgs = [i for i in l if '_BG.jpg' in i]
    ims = [i for i in l if '_BG.jpg' not in i]
    if date is not None:
        ims = [i for i in ims if
             timestr_to_delta(i.replace('_', ':').split('.')[0]).date() == date]
    return ims, bgs


def get_background_for_im(im, bgs):
    imt = im.split('.')[0].replace('_', ':')
    imtd = timestr_to_delta(imt)
    bg_times = [timestr_to_delta(bg.split('_BG.')[0].replace('_', ':')) for bg in bgs
                if (imtd - timestr_to_delta(bg.split('_BG.')[0].replace('_', ':'))).total_seconds() >= 0]
    bg = str(np.max(bg_times)).replace(':', '_') + '_BG.jpg'
    return bg


if __name__ == '__main__':
    import os
    os.chdir(r'C:\Users\Kristof\Desktop\testPi\photos')
    ims, bgs = get_images_and_backgrounds()
    ax = int(round(np.sqrt(len(ims))))+1
    out = np.zeros((ax*128, ax*128, 3)).astype('uint8')
    for i, im in enumerate(ims):
        ind = np.unravel_index(i, (ax, ax))
        bg = get_background_for_im(im, bgs)
        s = extract_subject(im, bg, pad=500)
        if s is not None:
            out[128*ind[0]:128*ind[0]+128, 128*ind[1]:128*ind[1]+128, :] = s
    plt.imshow(out)