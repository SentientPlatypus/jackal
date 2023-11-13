import cv2
import os
import time
import datetime
from joblib import dump, load
import numpy as np
from skimage.transform import resize
print("WE OUT")


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

print("loading model")
clfloaded = load(r"W:\Code\workorinternship\jackal\shadowsense-training\ad_hoc\ad_hoc\classifiers\super.joblib")

cap = cv2.VideoCapture(1)

print("starting stream...")
while cap.isOpened():
    success, img = cap.read()
    current_datetime = datetime.datetime.now()
    if not success:
        continue
    
    o, prediction = predict_image_opencv(clfloaded, img)

    cv2.putText(img, str(prediction), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 1,1)
    cv2.imshow("livefeed", img)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
