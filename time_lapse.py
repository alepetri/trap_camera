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

def images_to_video(videoWriter, image_dir, clear_images=True):
    image_list = glob.glob(f"{image_dir}/*.tiff")
    sorted_images = sorted(image_list, key=os.path.getmtime)
    for file in sorted_images:
        image_frame = cv2.imread(file)
        videoWriter.write(image_frame)
    if clear_images:
        for file in image_list:
            os.remove(file)

# initializing the camera
cap = cv2.VideoCapture(0)

width = int(vcap.get(cv2.cv.CAP_PROP_FRAME_WIDTH))
height = int(vcap.get(cv2.cv.CAP_PROP_FRAME_HEIGHT))

# initializing unique paths and names to save photos
now = datetime.datetime.now()
path = '/home/pi/Desktop/%02d%02d%04d_%02d_%02d_%02d' % (now.month, now.day, now.year, now.hour, now.minute, now.second)

if not os.path.exists(path):
    os.mkdir(path)

# initializing the VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter(f"{path}/timelapse.avi", fourcc, 20, (width, height))

finish_time = now + datetime.timedelta(seconds=100)
i = 0
while datetime.datetime.now() < finish_time:
    filename = f"{path}/{i}.tiff"
    ret, frame = cap.read()
    i += 1

    cv2.imwrite(filename,frame)

    time.sleep(0.5)

images_to_video(out, path, False)
# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()
