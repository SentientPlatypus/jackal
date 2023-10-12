import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from std_msgs.msg import Bool
from joblib import dump, load
from skimage.transform import resize
import numpy as np

            
class Camera(object):

    def __init__(self):
        self.height = 640
        self.width = 480
        self.fps = 10

        self.bridge = CvBridge()
        self.pubstr = "/shadowsense/is_touched"
        self.listeningto = "/shadowsense/camera/raw"
        rospy.init_node("datarecorder", anonymous=True)
        
        self.mode = "touch"
        self.touchDirectory = "trainingdata/touch"
        self.noTouchDirectory="trainingdata/no_touch"

        self.cap = cv2.VideoCapture(0)

    def listen():
        rospy.Subscriber(self.listeningto, Image, self.run)


    def run(self, image):
        cv_image = self.bridge.imgmsg_to_cv2(image, "bgr8")
        o, prediction = predict_image_opencv(self.clf, cv_image)
        path = touchDirectory if mode == "touch" else noTouchDirectory
        filename = "{}/frame{}.jpg".format(path, current_datetime.strftime("%Y%m%d_%H%M%S"))
        cv2.imwrite(filename, img)

if __name__ == '__main__':
    rospy.init_node("Publish_camera")
    camera = Camera()
    r = rospy.Rate(1)

    while not rospy.is_shutdown():
        camera.listen()
        r.sleep()
