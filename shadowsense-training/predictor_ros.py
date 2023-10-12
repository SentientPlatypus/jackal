import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from std_msgs.msg import Bool
from joblib import dump, load
from skimage.transform import resize
import numpy as np

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



class Camera(object):

    def __init__(self):
        self.height = 640
        self.width = 480
        self.fps = 10

        self.bridge = CvBridge()

        self.pubstr = "/shadowsense/is_touched"
        self.listeningto = "/shadowsense/camera/raw"
        rospy.init_node("predictor", anonymous=True)


        self.rawpub = rospy.Publisher(self.pubstr, Bool, queue_size=10)

        self.clf = load("yuhan_classifier/ad_hoc/ad_hoc/classifiers/super.joblib")

    def listen(self):
        rospy.Subscriber(self.listeningto, Image, self.run)
        rospy.spin()

    def run(self, image):
        cv_image = self.bridge.imgmsg_to_cv2(image, "bgr8")
        o, prediction = predict_image_opencv(self.clf, cv_image)
        print(prediction)
        touching = Bool()
        touching.data = int(prediction) == 0
        self.rawpub.publish(touching)

if __name__ == '__main__':
    camera = Camera()
    r = rospy.Rate(10)

    camera.listen()
