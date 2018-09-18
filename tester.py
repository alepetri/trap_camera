# importing camera interface, gpio interface, time, OpenCV2 image processing
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from datetime import datetime
import cv2
import os
from gpiozero import LED, MotionSensor
import sys

# initializing the camera, gpio pins, and path to save photos
led = LED(17)
pir = MotionSensor(21)
camera = PiCamera()
rawCapture = PiRGBArray(camera)
#camera.resolution = (640, 480)
#camera.framerate = 32
#rawCapture = PiRGBArray(camera, size=(640, 480)))
path = '/media/pi/TRAP_PIX'

# allows camera time to boot
time.sleep(0.1)

picture_count = 0
photo_taken = False

while picture_count < 50:
    if pir.motion_detected:
        led.on
        if not photo_taken:
            camera.capture(rawCapture, format="bgr")
            img = rawCapture.array
            now = datetime.now()
            current_pic_name = '%02d%02d%04d_%02d_%02d_%02d.jpg' % (now.month, now.day, now.year, now.hour, now.minute, now.second)
            cv2.imwrite(os.path.join(path, current_pic_name), img)
            photo_taken = True
            picture_count += 1
            print('Photos Taken: ' + str(picture_count))
    else:
        led.off
        photo_taken = False
