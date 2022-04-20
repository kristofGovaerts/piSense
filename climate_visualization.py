import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from scipy.ndimage.filters import gaussian_filter1d

LOCATION = r'C:\Users\Kristof\Desktop\testPi'


if __name__ == '__main__':
    df = pd.read_csv(os.path.join(LOCATION, 'climate_log.csv'), sep='\t')
    df['temperature'] = gaussian_filter1d(pd.to_numeric(df['temperature'], errors='coerce'), sigma=2)
    df['humidity'] = gaussian_filter1d(pd.to_numeric(df['humidity'], errors='coerce'), sigma=2)
    df['time'] = pd.to_datetime(df['time'])

    fig, ax = plt.subplots(ncols=2)
    g1 = sns.lineplot('time', 'temperature', data=df, ax=ax[0])
    ax[0].tick_params(labelrotation=45)
    g2 = sns.lineplot('time', 'humidity', data=df, ax=ax[1])
    ax[1].tick_params(labelrotation=45)
