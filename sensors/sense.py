import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def sense_light(i, duration):
    GPIO.setup(i, GPIO.IN)
    lOld = not GPIO.input(i)  # previous measurement
    print("Measuring ambient light for {} seconds.".format(duration))
    time.sleep(0.5)
    end = time.time() + duration

    while time.time() < end:
        if GPIO.input(i) != lOld:
            if GPIO.input(i):
                print(GPIO.input(i))
            else:
                print('no light')
        lOld = GPIO.input(i)
        time.sleep(0.2)


if __name__ == '__main__':
    sense_light(27, 5)
