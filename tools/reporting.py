import sys
import requests
import numpy as np
import datetime
from filestack import Client
from tools.extract import get_images_and_backgrounds, get_background_for_im, extract_subject


def save_report():
    with open('log.csv', 'w') as f:
        columns = ['time', 'temperature', 'humidity', 'is_active']
        s = '\t'.join(columns) + '\n'
        f.write(s)


def add_line(pars):
    with open('log.csv', 'a') as f:
        s = '\t'.join([str(p) for p in pars]) + '\n'
        f.write(s)


def read_keys():
    """Reads the key.txt file from the root folder."""
    with open('keys.txt', 'r') as f:
        k1 = f.readline()
        k2 = f.readline()
    return k1, k2


def send_alert(c1, c2):
    """Test"""
    # should add camera code here

    key1, key2 = [k.split('\n')[0] for k in read_keys()]

    # filestack code:
    client = Client(key2)
    new_filelink = client.upload(filepath=c1).url

    u = r'https://maker.ifttt.com/trigger/trigger/with/key/' + key1
    j = {"value1" : new_filelink,
         "value2" : c2}

    r = requests.post(u, json=j)
    if r.status_code == 200:
        print("Alert Sent")
    else:
        print("Error")


def mosaic_for_date(date, folder=''):
    ims, bgs = get_images_and_backgrounds(date=date, folder=folder)
    ax = int(round(np.sqrt(len(ims))))+1
    out = np.zeros((ax*128, ax*128, 3)).astype('uint8')

    for i, im in enumerate(ims):
        msg = "item {} of {}".format(i+1, len(ims))
        print(msg)

        ind = np.unravel_index(i, (ax, ax))
        bg = get_background_for_im(im, bgs)
        s = extract_subject(im, bg, pad=500)
        if s is not None:
            out[128*ind[0]:128*ind[0]+128, 128*ind[1]:128*ind[1]+128, :] = s
    return out
