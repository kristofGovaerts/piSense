import cv2


def bgr2gray(im):
    """
    BGR to grayscale conversion (shorthand).
    :param im: A 3-channel (BGR) image.
    :return: A grayscale image.
    """
    return cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)


def rgb2gray(im):
    """
    RGB to grayscale conversion (shorthand).
    :param im: A 3-channel (RGB) image.
    :return: A grayscale image.
    """
    return cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)


def bgr2rgb(im):
    """
    BGR to RGB conversion (shorthand).
    :param im: A 3-channel (BGR) image.
    :return: A 3-channel (RGB) image.
    """
    return cv2.cvtColor(im, cv2.COLOR_BGR2RGB)


def rgb2bgr(im):
    """
    RGB to BGR conversion (shorthand).
    :param im: A 3-channel (RGB) image.
    :return: A 3-channel (BGR) image.
    """
    return cv2.cvtColor(im, cv2.COLOR_RGB2BR)


def resize_rectangle(x, y, w, h, dims_in, dims_out):
    """
    Resizes a rectangle for dims_in to occupy the same relative position in a matrix of dims_out.
    :param x: An int. X0.
    :param y: An int. Y0.
    :param w: Rectangle width.
    :param h: Rectangle height.
    :param dims_in: Dimensions of image matrix for which the rectangle was initially computed.
    :param dims_out: Dimensions of output matrix for which the rectangle should fit.
    :return: Recalculated x, y, w, h values.
    """
    xr = dims_out[0]/dims_in[0]
    yr = dims_out[1]/dims_in[1]

    x2 = int(round(x * xr))
    y2 = int(round(y * yr))
    w2 = int(round(w * xr))
    h2 = int(round(h * yr))

    return x2, y2, w2, h2
