import matplotlib.pyplot as plt
import pandas as pd


if __name__ == '__main__':
    df = pd.read_csv('climate_log.csv', sep='\t')
    df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
    df['humidity'] = pd.to_numeric(df['humidity'], errors='coerce')
    df['time'] = pd.to_datetime(df['time'])

    plt.subplot(121)
    plt.plot(df['time'], df['temperature'])
    plt.subplot(122)
    plt.plot(df['time'], df['humidity'])