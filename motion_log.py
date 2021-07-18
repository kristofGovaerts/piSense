"""
this code senses motion, and activates LEDs & provides environment stats when activated.
"""
from output.led_control import activate_leds
from sensors.sense import sense_temp_hum, sense_motion
import time

PIR_PIN = 23  # motion detector
DHT11_PIN = 17  # temp/hum
GREEN_PIN = 26  # green led
RED_PIN = 16  # red led

while True:
    if sense_motion(PIR_PIN):
        activate_leds([GREEN_PIN], [2])
        h, t = sense_temp_hum(DHT11_PIN, wait=0)
        print("""Temperature: {}, humidity: {}""")

    time.sleep(1)
