import numpy as np
import cv2
from skimage.transform import resize
from joblib import load
from imutils.video import WebcamVideoStream
from skimage import color
from robot_mind import Robotmind
from playsound import playsound
import serial_interface
import time

# Start web camera stream
print("start video...")
stream = WebcamVideoStream(src='rtsp://admin@192.168.0.100:554/12').start()  # default camera
#stream = WebcamVideoStream(src='http://yuhan:yuhan@192.168.10.1/media/?action=stream').start()
#stream = WebcamVideoStream(src='http://admin:yuhan@199.168.1.149/media/?action=stream').start()
#stream = WebcamVideoStream(src='http://admin:@199.168.1.149/media/?action=stream').start()
print('connected')
# Start robot mind
robot = Robotmind('11-5.joblib')
#led = serial_interface.LED_Interface('/dev/cu.SLAB_USBtoUART')
#led.color('white')
#playsound('ask.mp3')

def get_video_frame():
    colorframe = stream.read()
    grayframe = color.rgb2gray(colorframe)
    #crop the video and leave only the middle area
    #cropped = grayframe[500:1500, 600:1300]
    #print(cropped.shape)
    #resized = resize(colorframe, (900,1300), mode= 'constant')

    resized_2 = resize(grayframe, (500, 500), mode='constant')
    cropped = resized_2[100:460, 100:350]
    resized = resize(cropped, (100, 100), mode='constant')
    displayed = resize(cropped, (500, 500), mode='constant')
    flattened = resized.flatten()
    return displayed, flattened[np.newaxis, :]
    #return resized


def label_frame(frame, classification):
    cv2.putText(frame, classification, (50, 50), cv2.FONT_ITALIC, 0.8, 255)
    cv2.imshow('frame', frame)
    cv2.waitKey(10)

# Main Loop


while True:
    # led.color('green')
    # time.sleep(5)
    # led.color('white')
    # time.sleep(5)
    #led.close()

    # Read and pre-process frame - resize and flatten
    frame, buffer = get_video_frame()
    #frame = get_video_frame()
    print(frame.shape)

    # Update robot state with flattened frame buffer
    interaction = robot.update_state(buffer)
    #interaction = "0"

    # Speak robot's response
    #robot.speak_help()
    # robot turn on the LED...
    #robot.light_on(led)
    #robot.speak_and_display()
    robot.speak_ouch()

    # Show classification on video display
    label_frame(frame, interaction)

