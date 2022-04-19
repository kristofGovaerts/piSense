"""
this code senses the room temperature and humidity and generates a time profile chart.
"""

import adafruit_dht
import time
from sensors.sense import sense_temp_hum, sense_motion
from output.reporting import *
from tools.time import current_time, is_active, timestr_to_delta

# globals
TIME_INTERVAL = 600  # one check each ten minutes
FILENAME = 'climate_log.csv'

# define pins
DHT11_PIN = 17  # temp/hum

# initialize sensors
sensor = adafruit_dht.DHT11(DHT11_PIN)

# initialize reporting
if not os.path.exists(FILENAME):
    save_report(filename=FILENAME, colnames=['time', 'temperature', 'humidity'])  # initialize file if doesn't exist. Otherwise, append existing
current_name = current_time()
last_check = timestr_to_delta(current_time())

while True:
    h, t = sense_temp_hum(sensor, wait=0)
    ts = current_time()  # timestamp as str
    tdelt = timestr_to_delta(ts)

    output = """Timestamp: {} --- Temperature: {}, humidity: {}"""

    print(output.format(ts, t, h))
    add_line([ts, t, h], filename=FILENAME)
    time.sleep(TIME_INTERVAL)
