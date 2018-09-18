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
camera = PiCamera()
rawCapture = PiRGBArray(camera)
path = '/media/pi/TRAP_PIX'

# allows camera time to boot
time.sleep(0.1)

camera.capture(rawCapture, format="bgr")
img = rawCapture.array
now = datetime.now()
current_pic_name = '%02d%02d%04d_%02d_%02d_%02d.raw' % (now.month, now.day, now.year, now.hour, now.minute, now.second)
cv2.imwrite(path + current_pic_name, img)
