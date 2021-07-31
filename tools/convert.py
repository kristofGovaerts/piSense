import cv2


def bgr2gray(im):
    return cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)


def rgb2gray(im):
    return cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)


def bgr2rgb(im):
    return cv2.cvtColor(im, cv2.COLOR_BGR2RGB)


def rgb2bgr(im):
    return cv2.cvtColor(im, cv2.COLOR_RGB2BR)


def resize_rectangle(x, y, w, h, dims_in, dims_out):
    xr = dims_out[0]/dims_in[0]
    yr = dims_out[1]/dims_in[1]

    x2 = int(round(x * xr))
    y2 = int(round(y * yr))
    w2 = int(round(w * xr))
    h2 = int(round(h * yr))

    return x2, y2, w2, h2
