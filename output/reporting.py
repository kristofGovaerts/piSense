import requests
import numpy as np
import datetime
from filestack import Client
from tools.extract import get_images_and_backgrounds, get_background_for_im, extract_subject
import pandas as pd
import matplotlib.dates as mdates
import cv2
import os


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


def mosaic_for_date(date=datetime.date.today(), folder=''):
    ims, bgs = get_images_and_backgrounds(date=date, folder=folder)
    ax1 = int(np.ceil(np.sqrt(len(ims))))
    ax2 = int(np.ceil(np.sqrt(len(ims))))
    out = np.zeros((ax2*128, ax1*128, 3)).astype('uint8')

    for i, im in enumerate(ims):
        msg = "item {} of {}".format(i+1, len(ims))
        print(msg)

        ind = np.unravel_index(i, (ax1, ax2))
        bg = get_background_for_im(im, bgs)
        s = extract_subject(im, bg, pad=500)
        if s is not None:
            out[128*ind[0]:128*ind[0]+128, 128*ind[1]:128*ind[1]+128, :] = s
        out = cv2.putText(out, str(i), (128*ind[1]+20, 128*ind[0]+20),
                          fontFace = cv2.FONT_HERSHEY_COMPLEX, fontScale = 1, color = (250,225,100))
    return out


def log_for_date(date=datetime.date.today(), freq='30min', filename='log.csv'):
    df = pd.read_csv(filename, sep='\t')
    df['datetime'] = pd.to_datetime(df['time'])
    df['date'] = [d.date() for d in df['datetime']]
    df['time'] = [d.time() for d in df['datetime']]

    dff = df[df['date']==date]
    dff = dff.replace('None', None)
    dff.temperature = pd.to_numeric(dff.temperature)
    dff.humidity = pd.to_numeric(dff.humidity)

    dffm = dff.groupby(pd.Grouper(key='datetime', freq=freq))\
        .agg({'time':'count',
              'temperature':'mean',
              'humidity': 'mean'}).rename(columns={'time':'activations'})
    return pd.DataFrame(dffm)


def plot_for_date(date=datetime.date.today()):
    d = log_for_date(date=date)
    d['time'] = d.index

    fig, ax = plt.subplots(1,2, figsize = (14,6), sharey=True)
    hues=['orange', 'blue']
    xfmt = mdates.DateFormatter('%H:%M')

    for i, p in enumerate(('temperature', 'humidity')):
        ax[i].plot_date(d.time, d["activations"], color="red", label="activations", linestyle="-")
        ax[i].xaxis.set_major_formatter(xfmt)

        ax2 = ax[i].twinx()
        ax2.plot(d['time'], d[p],color=hues[i], label=p)

        h1, l1 = ax[i].get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax[i].legend(h1 + h2, l1 + l2)
        ax2.xaxis.set_major_formatter(xfmt)

        ax[i].set_ylabel('# activations')
        ax2.set_ylabel(p)
    fig.suptitle(date, fontsize=30)
    fig.savefig(str(date) + '_plot.png')


if __name__ == '__main__':
    os.chdir(r'C:\Users\Kristof\Desktop\testPi\photos')
    o = mosaic_for_date()
    cv2.imwrite('mosaic.jpg', o)
