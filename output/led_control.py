import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
LED = 16
ledState = False
GPIO.setup(LED, GPIO.OUT)

try:
    while True:
        ledState = not ledState
        GPIO.output(LED, ledState)
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Shutting down.")
    ledState = False
    GPIO.output(LED, ledState)