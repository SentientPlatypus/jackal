from train_classifier2 import Trainer, TrainerExited
from joblib import dump, load
import cv2
import numpy as np
from skimage.io import imread
from skimage.transform import resize
from skimage import color, img_as_float
import time



def predict_image_opencv(clf, opencv_image):
    w, h, _ = opencv_image.shape  # Get the width and height of the image

    opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale if needed

    buffer = np.frombuffer(opencv_image.tobytes(), dtype=np.uint8)
    buffer = np.reshape(buffer, (h, w))

    buffer = resize(buffer, (100, 100))
    buffer = buffer.flatten()
    buffer = buffer[np.newaxis, :]

    pred = clf.predict(buffer)[0]
    return buffer, pred


clfloaded = load(r"classifiers\super.joblib")


opencv_image = cv2.imread(r"/home/david/catkin_ws/src/jackal/shadowsense-training/trainingdata/no_touch/frame20230911_172246.jpg")


classification_result = predict_image_opencv(clfloaded, opencv_image)
original_image,prediction = classification_result
print('predicted', prediction)
