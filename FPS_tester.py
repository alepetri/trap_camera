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
camera.resolution = (640, 480)
camera.framerate = 60
#rawCapture = PiRGBArray(camera, size=(640, 480)))
now = datetime.now()
path = '/media/pi/TRAP_PIX/%02d%02d%04d_%02d_%02d_%02d' % (now.month, now.day, now.year, now.hour, now.minute, now.second)

if not os.path.exists(path):
    os.makedirs(path)

# allows camera time to boot
time.sleep(0.1)

picture_count = 0
before = time.time()
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    if picture_count >= 100:
        break

    #camera.capture(rawCapture, format="bgr")
    img = frame.array
    #now = datetime.now()
    #current_pic_name = '%02d%02d%04d_%02d_%02d_%02d_%02d.jpg' % (now.month, now.day, now.year, now.hour, now.minute, now.second, now.microsecond)
    current_pic_name = '%02d.jpg' % (picture_count)
    cv2.imwrite(os.path.join(path, current_pic_name), img)
    picture_count += 1
    #print('Photos Taken: ' + str(picture_count))
    rawCapture.truncate(0)
    
    time.sleep(0.001)

print(time.time()-before)
