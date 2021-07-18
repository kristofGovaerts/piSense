"""
this code senses motion, and activates LEDs & provides environment stats when activated.
"""
from output.led_control import activate_leds
from sensors.sense import sense_temp_hum, sense_motion
import adafruit_dht
import RPi.GPIO as GPIO
import time
from tools.time import current_time

PIR_PIN = 23  # motion detector
DHT11_PIN = 17  # temp/hum
GREEN_PIN = 26  # green led
RED_PIN = 16  # red led

# initialize sensors
sensor = adafruit_dht.DHT11(DHT11_PIN)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(RED_PIN, GPIO.OUT)

while True:
    # todo: respond to high-frequency motion by changing led color.
    if sense_motion(PIR_PIN):
        activate_leds([GREEN_PIN], [2])
        h, t = sense_temp_hum(sensor, wait=0)
        ts = current_time()  # timestamp as str
        print("""Timestamp: {} --- Temperature: {}, humidity: {}""".format(ts, t, h))

    time.sleep(1)
