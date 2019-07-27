# importing camera interface, gpio interface, time, OpenCV2 image processing
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import datetime
import cv2
import os
from gpiozero import LED, MotionSensor, Button
import sys
from subprocess import call

import glob


def blink(LED, secs_between_blinks, num_blinks):
    count = 0
    while count < num_blinks*2:
        LED.toggle()
        time.sleep(secs_between_blinks/2)
        count += 1
    return


def images_to_video(videoWriter, image_dir, clear_images=True):
    image_list = glob.glob(f"{image_dir}/*.jpg")
    sorted_images = sorted(image_list, key=os.path.getmtime)
    for file in sorted_images:
        image_frame = cv2.imread(file)
        videoWriter.write(image_frame)
    if clear_images:
        for file in image_list:
            os.remove(file)


# initializing the gpio pins
ir_illuminator = LED(14, active_high=False)
ir_illuminator.off()
LED_indicator = LED(4)
LED_indicator.off()
passive_infrared = MotionSensor(27)
button = Button(17, hold_time=3)

# initializing the camera
cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# initializing unique paths and names to save photos
now = datetime.datetime.now()
#path = '/home/pi/Desktop/%02d%02d%04d_%02d_%02d_%02d' % (now.month, now.day, now.year, now.hour, now.minute, now.second)
folder_path = '/media/pi/TRAP_PIX/%02d%02d%04d_%02d_%02d_%02d' % (now.month, now.day, now.year, now.hour, now.minute, now.second)
while not os.path.ismount('/media/pi/TRAP_PIX'):
    print("can't find")
    time.sleep(2)
else:
    print("flash drive found")
    os.makedirs(folder_path)
    print("made folder")

# initializing the VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter(f"{path}/timelapse.avi", fourcc, 20, (width, height))

LED_indicator.on()

while not button.is_held:
    pass

blink(LED_indicator, 0.5, 60)
LED_indicator.off()


finish_time = now + datetime.timedelta(seconds=100)
i = 0
while now < finish_time:
    if now > last_pic + datetime.timedelta(seconds=1):
        print(i)
        filename = f"{path}/{i}.jpg"
        ret, frame = cap.read()
        i += 1

        cv2.imwrite(filename,frame)

    now = datetime.datetime.now()

images_to_video(out, path)
# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()
