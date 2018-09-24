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
now = datetime.now()
path = '/media/pi/TRAP_PIX/%02d%02d%04d_%02d_%02d_%02d' % (now.month, now.day, now.year, now.hour, now.minute, now.second)
if not os.path.exists(path):
    os.makedirs(path)

# allows camera time to boot
time.sleep(0.1)

picture_count = 0
group_number = 1
in_same_group = True
time_at_motion = 0
time_since_motion = 0

while picture_count < 13000:
    if pir.motion_detected:
        led.on
        time_at_motion = time.time()
    else:
        led.off

    time_since_motion = time.time() - time_at_motion

    if time_since_motion < 10:
        if not in_same_group:
            group_number += 1
            in_same_group = True
        camera.capture(rawCapture, format="bgr")
        img = rawCapture.array
        now = datetime.now()
        current_pic_name = 'G%03d_%02d%02d%04d_%02d_%02d_%02d.jpg' % (group_number, now.month, now.day, now.year, now.hour, now.minute, now.second)
        cv2.imwrite(os.path.join(path, current_pic_name), img)
        picture_count += 1
        print('Photos Taken: ' + str(picture_count))
        rawCapture.truncate(0)
    else:
        in_same_group = False

    time.sleep(0.05)
