import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def activate_led(id, duration):
    GPIO.setup(id, GPIO.OUT)
    GPIO.output(id, True)
    time.sleep(duration)
    GPIO.output(id, False)


if __name__ == '__main__':
    activate_led(16, 5)
    activate_led(26, 10)