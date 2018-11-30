# importing camera interface, gpio interface, time, OpenCV2 image processing
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from datetime import datetime
import cv2
import os
from gpiozero import LED, MotionSensor, Button
import sys

# 
def blink(LED, secs_between_blinks, num_blinks):
    count = 0
    while count < num_blinks*2:
        LED.toggle()
        time.sleep(secs_between_blinks/2)
        count += 1
    return

# initializing the gpio pins
ir_illuminator = LED(14, active_high=False)
ir_illuminator.off()
LED_indicator = LED(4)
LED_indicator.off()
passive_infrared = MotionSensor(27)
button = Button(17, hold_time=3)

# initializing the camera
camera = PiCamera()
rawCapture = PiRGBArray(camera)


# initializing unique paths and names to save photos
now = datetime.now()
#path = '/home/pi/Desktop/%02d%02d%04d_%02d_%02d_%02d' % (now.month, now.day, now.year, now.hour, now.minute, now.second)
path = '/media/pi/TRAP_PIX/%02d%02d%04d_%02d_%02d_%02d' % (now.month, now.day, now.year, now.hour, now.minute, now.second)
if not os.path.exists(path):
    os.makedirs(path)

LED_indicator.on()

while not button.is_held:
    pass

blink(LED_indicator, 0.5, 20)
LED_indicator.off()

picture_count = 0
group_number = 0
in_same_group = False
time_at_motion = 0
time_since_motion = 0
while not button.is_held and picture_count < 400:
    if passive_infrared.motion_detected:
        time_at_motion = time.time()
        ir_illuminator.on()

    time_since_motion = time.time() - time_at_motion

    if time_since_motion < 10:
        if not in_same_group:
            group_number += 1
            in_same_group = True
        camera.capture(rawCapture, format="bgr")
        img = rawCapture.array
        now = datetime.now()
        current_pic_name = 'G%03d_%02d%02d%04d_%02d_%02d_%02d_%02d.jpg' % (group_number, now.month, now.day, now.year, now.hour, now.minute, now.second, now.microsecond)
        cv2.imwrite(os.path.join(path, current_pic_name), img)
        picture_count += 1
        #print('Photos Taken: ' + str(picture_count))
        rawCapture.truncate(0)
    else:
        in_same_group = False
        ir_illuminator.off()

    time.sleep(0.01)

ir_illuminator.off()
blink(LED_indicator, 1, 5)
LED_indicator.off()
