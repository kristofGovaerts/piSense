import RPi.GPIO as GPIO
import time
import Adafruit_DHT  # Tools for eading from the DHT sensor (temperature/humidity)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def sense_temp_hum(i):
    sensor = Adafruit_DHT.DHT11
    humidity, temperature = Adafruit_DHT.read_retry(sensor, i)
    return humidity, temperature


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
    #sense_light(27, 5)
    humidity, temperature = sense_temp_hum(17)
    if humidity is not None and temperature is not None:
        print(temperature, humidity)
        print('Temperature={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
        print('Failed to get reading from the sensor. Try again!')
