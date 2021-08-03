# piSense
## Introduction
This is a small project for developing a simple motion-activated activity tracker, as well as a reporting tool, both automatic (via notifications on smartphone) and on-demand (via Python code). 

### Problem statement
I've been raising a Roborovski dwarf hamster for the past few months, and I've noticed that it doesn't really *do* much. In particular, it doesn't seem to be using its hamster wheel at all, unlike the previous occupant of its cage, a Syrian gold hamster which ran around constantly when she was in good health. There are a few potential reasons for this discrepancy:
- The hamster wheel is too large. A Syrian hamster is ~100-120g whereas a dwarf hamster is only 20-25g - it's possible that the hamster wheel is simply too heavy for the little guy to move, and it might be necessary to purchase a new, smaller wheel.
- The preferred activity hours of the dwarf hamster don't align with my own time awake, and I simply don't notice him using his wheel. Of course, rodents are often more nocturnal, but it is a fact that our previous pet was active during the day quite often.

The straightforward way to tackle this problem is to stay up at night and see what's going on, but as a scientist I wanted a method that would allow me to track my pet's activity level in an automatic and preferably unbiased manner. I also want to answer several other questions:
- Do activity levels change depending on temperature/humidity levels? To answer this question, we will have acquire data across multiple months, as room temperature does not change much overnight.
- Is it possible to use a machine learning algorithm to identify what the animal is doing based on the shape of the segmentation, or is it better to just look at the relative position in the image? 
- Can I monitor the hamster's weight by using the amount of pixels as a proxy?

## Method
### Setup
For this experiment, we made use of a Raspberry Pi 4. A DHT11 temperature and humidity sensor was connected to *GPUI pin 17*, while the passive infrared (PIR) sensor was connected to *GPUI pin 23*. The camera module was connected to the board's camera port. 

The code is set up as follows:
- When the passive infrared (PIR) motion sensor detects motion, the camera starts acquiring images every second. If these images differ from the background by more than a threshold value, an alert is sent using the reporting APIs (upload image to Filestack and send to Telegram) which are linked in the keys.txt file, and the camera continues to acquire once per second until motion stops.
- When there is no motion, we refresh the background every two minutes to correct for differences in light intensity.
- For identifying where the subject is located in the image, we perform background subtraction, followed by a thresholding step. We can then identify the largest 'blob' in the image, which should be our subject, and extract this using OpenCV's bounding rectangle tool.
- For consistency, we also ensure that output subjects are all resampled to a size of 128x128, with zero-padding.

 ![Figure_1](/Figure_1.png)

## Logging
tools.reporting features several logging tools. For instance, using tools.reporting.plot_for_date() we can produce an activity plot for either the current date or any provided date in datetime format:

![dateplot](/2021-08-02_plot.png)

Here, we can clearly see that the subject hamster's peak activity times are at night, starting a bit before midnight and terminating around 6 - exactly the inverse of my own waking times. Temperature is remarkably stable. Humidity also stays relatively stable. Probably in the winter temperature will vary more overnight.

We can also produce a mosaic for quick inspection of photos taken, which allows for a quick evaluation of whether the quality of subject detection is okay:

![mosaic](/mosaic.jpg)

- There are a few images where no subject could be identified at all, but these are limited. Since we can see the index of these images in the mosaic, we can inspect these and see what went wrong.
- There are also a few images where the subject was not fully segmented, or where for example the hamster wheel was (incorrectly) identified as the subject. Evidently there is still some room for improvement!

## Materials
### Necessary:
- Raspberry Pi 4 Model B (other models should work too)
- 1x DHT11 temperature & humidity sensor
- 1x HC-SR501 PIR motion sensor
- 1x Raspberry Pi Camera module with IR lights (any)
- A subject to image! In this case, we use a Roborovski dwarf hamster but in principle anything that moves can be used, as long as you are using a camera that captures their habitat.

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
- pandas
- imutils
- RPi
