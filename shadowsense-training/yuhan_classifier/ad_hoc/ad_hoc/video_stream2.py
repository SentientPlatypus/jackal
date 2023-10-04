import time
import numpy as np
import cv2
from ad_hoc.train_classifier2 import Trainer, TrainerExited
from skimage.transform import resize
from joblib import dump, load
from imutils.video import WebcamVideoStream
from skimage import color, img_as_float
from robot_mind import Robotmind

stream = WebcamVideoStream(src='rtsp://admin@192.168.0.100:554/12').start()  # default camera
print("loading classifier..")
clf = load('touch-hug.joblib')
print("start video...")
robot = Robotmind()

while True:
    frame = stream.read()
    frame = color.rgb2gray(frame)
    buffer = resize(frame, (100, 200), mode='constant')
    buffer = buffer.flatten()
    buffer = buffer[np.newaxis, :]
    pred = clf.predict(buffer)[0]
    robot.update_state(pred)
    k = robot.label_pred(pred)
    cv2.putText(frame, k, (50, 50), cv2.FONT_ITALIC, 0.8, 255)
    cv2.imshow('frame', frame)
    cv2.waitKey(10)
    robot.speak()

    # from ffpyplayer.pic import SWScale, Image
    # from ffpyplayer.player import MediaPlayer

    # lib_opts = {}
    # ff_opts = {'f':'rtsp'}
    # player = MediaPlayer('rtsp://admin@192.168.0.100:554/12',
    #                      ff_opts=ff_opts)

    # trainer = Trainer(train_path="data/trainer_touch/", test_path="data/tester_touch/")
    # trainer.train()
    # if val == 'eof':
    #     break
    # elif frame is None:
    #     time.sleep(0.1)
    # else:
    #     img, t = frame
    #     fmt = img.get_pixel_format()
    #     scaler = SWScale(*img.get_size(), fmt, ofmt='gray')
    #     image = scaler.scale(img)
    #     #print(val, t, img.get_pixel_format(), img.get_buffer_size())
    #     buffer = np.frombuffer(image.to_bytearray()[0], dtype=np.uint8)
    #     w, h = image.get_size()
    #     buffer = np.reshape(buffer, (h, w))
        # #buffer = resize(buffer, (100, 200))
        # #bu, pred = trainer.predict_image(img)
        #
        # bu = resize(buffer, (100, 200), mode='constant')
        # bu = bu.flatten()
        # bu = bu[np.newaxis, :]
        #
        # pred = clf.predict(bu)[0]
        # if pred == 0:
        #     k = "hugging"
        #     playsound('ouch2.mp3')
        #     print("finish playing")
        # elif pred == 1:
        #     k = "not touching"
        # elif pred == 2:
        #     k = "touching"
        # # elif pred == 3:
        # #     k = "ouch!!"
        # # elif pred == 4:
        # #     k = "touching"
        # #print(pred)
        # cv2.putText(buffer, k, (50, 50), cv2.FONT_ITALIC, 0.8, 255)
        # cv2.imshow('Video', buffer)
        # cv2.waitKey(10)
        #time.sleep(10)