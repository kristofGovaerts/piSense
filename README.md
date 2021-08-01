# piSense
## Introduction
This is a small project for developing a simple motion-activated activity tracker. The idea is to produce different types of output depending on the type (particularly frequency) of motion that is detected. Will also double as a security camera later on. In time I'll add some nice-looking reports.

## Method
- When the passive infrared (PIR) motion sensor detects motion, the camera starts acquiring images every second. If these images differ from the background by more than a threshold value, an alert is sent using the APIs which are linked in the keys.txt file, and the camera continues to acquire once per second until motion stops.
- When there is no motion, we refresh the background every two minutes to correct for differences in light intensity.
- For identifying where the subject is located in the image, we perform background subtraction, followed by a thresholding step. We can then identify the largest 'blob' in the image, which should be our subject, and extract this using OpenCV's bounding rectangle tool.
- For consistency, we also ensure that output subjects are all resampled to a size of 128x128, with zero-padding.

 ![Figure_1](/Figure_1.png)

## Logging
tools.reporting features several logging tools. For instance, using tools.reporting.plot_for_date() we can produce an activity plot for either the current date or any provided date in datetime format:

![dateplot](/2021-08-01_plot.png)

Here, we can clearly see that the subject hamster's peak activity times are between 1AM And 2AM. Although temperature drops over time, the change is very minor. Humidity also stays relatively stable. Probably in the winter temperature will vary more overnight.

We can also produce a mosaic for quick inspection of photos taken, which allows for a quick evaluation of whether the quality of subject detection is okay:

![mosaic](/mosaic.jpg)

- There are a few images where no subject could be identified at all, but these are limited. Since we can see the index of these images in the mosaic, we can inspect these and see what went wrong.
- There are also a few images where the subject was not fully segmented, or where for example the hamster wheel was (incorrectly) identified as the subject. Evidently there is still some room for improvement!

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
