
import time
import os
from gpiozero import LED, MotionSensor
import sys

# initializing the camera, gpio pins, and path to save photos
led = LED(14)

# allows camera time to boot
time.sleep(0.1)


time_before = time.time()
time_current = time_before
print(time_before)

while time_current < time_before + 60:
    led.on()
    print("on")
    time.sleep(5)
    led.off()
    print("off")
    time.sleep(5)
    time_current = time.time()

  