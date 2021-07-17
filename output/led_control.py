import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def activate_leds(ids, durations):
    for n, i in enumerate(ids):
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, True)
        time.sleep(durations[n])
        GPIO.output(i, False)


if __name__ == '__main__':
    # test code
    activate_leds([16, 26], [5, 10])
