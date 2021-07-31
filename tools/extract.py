import cv2
import imutils
import numpy as np
from tools.convert import *


def extract_subject(im, bg, mode='rgb', output_size=128, buf=40):
    """
    Extracts a subje
    :param im:
    :param bg:
    :param mode:
    :param output_size:
    :param buf:
    :return:
    """
    img = cv2.imread(im)
    bgn = cv2.imread(bg)

    imgr = imutils.resize(img, width=bgn.shape[1])
    d = np.abs(bgr2gray(imgr).astype('float')/255-bgr2gray(bgn).astype('float')/255)
    db = cv2.GaussianBlur(d, (21,21), 0)
    db[db<0.1] = 0
    db[db>=0.1] = 1
    contours, hierarchy = cv2.findContours(db.astype('uint8'), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    try:
        largest_contour = contours[np.argmax([len(c) for c in contours])]
        x, y, w, h = cv2.boundingRect(largest_contour)
        x, y, w, h = resize_rectangle(x, y, w, h, imgr.shape, img.shape, make_square=True)

        print(x, y, w, h)
        print(img.shape)
        if x + w + buf > img.shape[1]:
            xl = img.shape[1]
        else:
            xl = x + w + buf

        if y + h + buf > img.shape[0]:
            yl = img.shape[0]
        else:
            yl = y + h + buf
        out = img[y-buf:yl, x-buf:xl, :]
        print(out.shape)

        out = imutils.resize(out, width=output_size)
        if mode == 'gray':
            out = bgr2gray(im)
    except ValueError:
        print("No subject found.")
        out = None
    return out


if __name__ == '__main__':
    import glob
    l=glob.glob(r'2021-07-31 09_49*')
    bg = r'2021-07-31 09_49_47_BG.jpg'

    for i in l:
        if '_D.jpg' not in i:
            s = extract_subject(i, bg)
            if s is not None:
                plt.figure()
                plt.imshow(s)