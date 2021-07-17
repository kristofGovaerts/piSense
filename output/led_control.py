import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def activate_leds(ids, durations):
    start = time.clock()
    now = time.clock()
    for n, i in enumerate(ids): # need a while loop
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, True)
        time.sleep(durations[n])
        GPIO.output(i, False)
        now = time.clock()


if __name__ == '__main__':
    # test code
    # doesn't do what it needs to do yet
    activate_leds([16, 26], [5, 10])
