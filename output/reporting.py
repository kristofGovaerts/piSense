import requests
import numpy as np
import datetime
from filestack import Client
from tools.extract import get_images_and_backgrounds, get_background_for_im, extract_subject
import pandas as pd
import matplotlib.dates as mdates
import cv2
import os
import matplotlib
matplotlib.use('Agg')  # turn off visualisation or matplotlib.pyplot doesn't work
import matplotlib.pyplot as plt


def save_report(filename='log.csv', delimiter='\t'):
    """
    Initializes the report file in the current directory.
    :return: Nothing, but a .csv file will be written.
    """
    with open(filename, 'w') as f:
        columns = ['time', 'temperature', 'humidity', 'is_active']
        s = delimiter.join(columns) + '\n'
        f.write(s)


def add_line(pars, filename='log.csv', delimiter='\t'):
    """
    :param pars: A list of parameters. Should correspond with the number of columns in the output file!
    :param filename: The filename for the log file. Default 'log.csv' in the active directory.
    :param delimiter: The delimiter for the output file. Default tab.
    :return: Nothing, but a line will be appended to the log file.
    """
    with open(filename, 'a') as f:
        s = delimiter.join([str(p) for p in pars]) + '\n'
        f.write(s)


def read_keys():
    """Reads the key.txt file from the root folder. This file should be provided by whichever user is
    managing the APIs for file storage and reporting."""
    with open('keys.txt', 'r') as f:
        k1 = f.readline()
        k2 = f.readline()
    return k1, k2


def send_alert(c1, c2=''):
    """
    Reporting code. This takes a local image address (c1), uploads it to Filestack, and sends the generated Filestack
    link and an annotation line c2 to Telegram via IFTTT.
    :param c1: A local image location.
    :param c2: An optional annotation string.
    :return:
    """
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
    """
    Generates an activity log for a particular date. A count of activations per time block (freq) as well as an average
    for each measurement for each of these blocks is calculated.
    :param date: A datetime.datetime object. Default today.
    :param freq: Time bin size. Default 30min.
    :param filename: The filename of the log file. Default 'log.csv' in the current active directory.
    :return: A pandas dataframe.
    """
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
    lims=((15,30),(30,60))

    for i, p in enumerate(('temperature', 'humidity')):
        ax[i].plot_date(d.time, d["activations"], color="red", label="activations", linestyle="-")
        ax[i].xaxis.set_major_formatter(xfmt)

        ax2 = ax[i].twinx()
        isf = np.isfinite(d[p])
        ax2.plot(d['time'][isf], d[p][isf], color=hues[i], label=p)
        ax2.set_ylim(lims[i])

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
    d=datetime.date(year=2021,month=8,day=2)
    plot_for_date(date=d)
    #o = mosaic_for_date(date=d)
    #cv2.imwrite('mosaic.jpg', o)
