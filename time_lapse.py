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
camera = PiCamera()
rawCapture = PiRGBArray(camera)

# initializing the VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'X246')
out = cv2.VideoWriter("name.AVCHD", fourcc, 20, (2592, 1944))

# initializing unique paths and names to save photos
now = datetime.now()
path = '/home/pi/Desktop/%02d%02d%04d_%02d_%02d_%02d' % (now.month, now.day, now.year, now.hour, now.minute, now.second)

if not os.path.exists(path):
    os.mkdir(path)

finish_time = now + datetime.timedelta(seconds=600)
i = 0
while datetime.datetime.now() < finish_time:
    filename = f"{path}/{i}.tiff"
    camera.capture(rawCapture, format="bgr")
    img = rawCapture.array
    cv2.imwrite(filename,img)
    rawCapture.truncate(0)
    time.sleep(0.01)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

images_to_video(out, path)
# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()
