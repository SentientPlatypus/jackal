#from skimage import io
#from imutils import paths
import argparse
#import imutils
import cv2
import os
from pathlib import Path
#import matplotlib.pyplot as plt
#import matplotlib.patches as patches
from threading import Thread, Lock, Condition
import numpy as np
from sklearn import svm, metrics, datasets
from sklearn.utils import Bunch
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, train_test_split

from skimage.io import imread
from skimage.transform import resize
from skimage import color, img_as_float
import time

from ffpyplayer.pic import SWScale, Image

__all__ = ('Trainer', 'TrainerExited')


class TrainerExited(Exception):
    pass


class Trainer(object):

    condition = None

    classify_condition = None

    next_image_to_classify = None

    classification_result = None

    thread = None

    _finish_running = False

    _finished_running = False

    image_scaler = None

    last_img_fmt = ''

    start_t = time.time()

    def __init__(self, train_path, test_path):
        print("loading dataset " + "...")
        image_dataset = load_image_files(train_path)
        test_dataset = load_image_files(test_path)
        self.X_train = image_dataset.data
        self.y_train = image_dataset.target
        self.X_test = test_dataset.data
        self.y_test = test_dataset.target
        self.accuracy = 0
        self.clf = None
        self.classify_condition = Condition()

    def train(self, train_model=True):
        if train_model:
            param_grid = [
                {'C': [1, 10, 100, 1000], 'kernel': ['linear']},
                {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']},
            ]
            svc = svm.SVC()
            self.clf = GridSearchCV(svc, param_grid, cv=5)
            print("training...")
            start_time = time.time()
            self.clf.fit(self.X_train, self.y_train)
            print(self.X_train.shape, self.y_train.shape)
            training_time = time.time() - start_time
            #print("training time = {0:.1f} sec".format(training_time))
            print("evaluating...")
            y_pred = self.clf.predict(self.X_test)
            print("y_pred",y_pred)
            #print("Classification report for - \n{}:\n{}\n".format(
             #   self.clf, metrics.classification_report(self.y_test, y_pred)))
            self.accuracy = accuracy_score(self.y_test, y_pred)
            print("accuracy: {0:.01f}".format(self.accuracy))
            return self.clf

    def predict_image(self, image):
        fmt = image.get_pixel_format()
        scaler = self.image_scaler

        if fmt != 'gray':
            if scaler is None or fmt != self.last_img_fmt:
                scaler = self.image_scaler = SWScale(
                    *image.get_size(), fmt, ofmt='gray')
                self.last_img_fmt = fmt
            image = scaler.scale(image)

        buffer = np.frombuffer(image.to_bytearray()[0], dtype=np.uint8)
        w, h = image.get_size()
        buffer = np.reshape(buffer, (h, w))
        #print(time.time()-self.start_t)
        #cv2.imshow('Video', buffer)

        buffer = resize(buffer, (100, 200), mode='constant')
        buffer = buffer.flatten()
        buffer = buffer[np.newaxis, :]

        pred = self.clf.predict(buffer)[0]
        return buffer, pred

    def predict_image_opencv(self, opencv_image):
        w, h, _ = opencv_image.shape  # Get the width and height of the image

        opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale if needed

        buffer = np.frombuffer(opencv_image.tobytes(), dtype=np.uint8)
        buffer = np.reshape(buffer, (h, w))

        buffer = resize(buffer, (100, 100))
        buffer = buffer.flatten()
        buffer = buffer[np.newaxis, :]

        pred = self.clf.predict(buffer)[0]
        return buffer, pred


def load_image_files(container_path, dimension=(64, 64)):
        """
        Load image files with categories as subfolder names
        which performs like scikit-learn sample dataset

        Parameters
        ----------
        container_path : string or unicode
            Path to the main folder holding one subfolder per category
        dimension : tuple
            size to which image are adjusted to

        Returns
        -------
        Bunch
        """
        image_dir = Path(container_path)
        folders = [directory for directory in image_dir.iterdir() if directory.is_dir()]
        categories = [fo.name for fo in folders]

        descr = "A image classification dataset"
        images = []
        flat_data = []
        target = []
        # keep track of the previous label
        i_previous = -1
        for i, direc in enumerate(folders):
            for file in direc.iterdir():
                try:
                    if file == '.DS_Store':
                        continue
                    img = imread(file)
                except ValueError:
                    continue

                # print out the file and the numeric label
                if i_previous is not i:
                    print(i)
                    print(file)
                    i_previous = i

                # img_resized = resize(img, dimension, anti_aliasing=True, mode='reflect')
                img = color.rgb2gray(img)
                #version 2 for test
                img = resize(img, (100, 100))
                #cropped = img[0:300, 150:500]
                #img = resize(cropped, (100, 100))

                flat_data.append(img.flatten())
                images.append(img)
                target.append(i)
        flat_data = np.array(flat_data)
        target = np.array(target)
        images = np.array(images)

        return Bunch(data=flat_data,
                     target=target,
                     target_names=categories,
                     images=images,
                     DESCR=descr)
