import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def activate_led(ids, durations):
    for n, i in enumerate(ids):
        GPIO.setup(id, GPIO.OUT)
        GPIO.output(id, True)
        time.sleep(durations[n])
        GPIO.output(id, False)


if __name__ == '__main__':
    # test code
    activate_leds([16, 26], [5, 10])
