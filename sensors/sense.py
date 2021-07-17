import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def sense_light(i, duration):
    GPIO.setup(i, GPIO.IN)
    lOld = not GPIO.input(i)  # previous measurement
    print("Measuring ambient light for {} seconds.".format(duration))
    time.sleep(0.5)
    start = time.clock()
    now = time.clock()

    while now < start + duration:
        if GPIO.input(i) != lOld:
            if GPIO.input(i):
                print('\u263e')
            else:
                print('\u263c')
        lOld = GPIO.input(LIGHT_PIN)
        time.sleep(0.2)


if __name__ == '__main__':
    sense_light(27, 5)