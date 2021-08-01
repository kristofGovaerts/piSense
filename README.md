# piSense
## Introduction
This is a small project for developing a simple motion-activated activity tracker. The idea is to produce different types of output depending on the type (particularly frequency) of motion that is detected. Will also double as a security camera later on. In time I'll add some nice-looking reports.

## Method
The camera refreshes the background every two minutes. When the passive infrared (PIR) motion sensor detects motion, the camera starts acquiring images every second. If these images differ from the background by more than a threshold value, an alert is sent using the APIs which are linked in the keys.txt file.

 ![Figure_1](/Figure_1.png)

## Logging
tools.reporting features several logging tools. For instance, using tools.reporting.plot_for_date() we can produce an activity plot for either the current date or any provided date in datetime format:

![dateplot](/2021-08-01_plot.png)

We can also produce a mosaic for quick inspection of photos taken, which allows for a quick evaluation of whether the quality of subject detection is okay:

![mosaic](/mosaic.jpg)

## Materials
### Necessary:
- Raspberry Pi 4 Model B 
- 1x DHT11 temperature & humidity sensor
- 1x HC-SR501 PIR motion sensor
- 1x Raspberry Pi Camera module with IR lights (any)

### Optional:
- Raspberry Pi T-Cobbler (40 pins)
- 400 points breadboard
- 1x red LED
- 1x green LED (could also use one RGB LED)
- 2x 100 Ohm resistor

## Dependencies
- numpy
- matplotlib
- adafruit_dht: https://github.com/adafruit/Adafruit_CircuitPython_DHT
- picamera
- opencv-python (cv2)
- imutils
- RPi
