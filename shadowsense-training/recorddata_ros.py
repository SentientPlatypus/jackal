import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from std_msgs.msg import Bool
from joblib import dump, load
from skimage.transform import resize
import numpy as np
import time
import datetime
            
class Camera(object):

    def __init__(self):
        self.height = 640
        self.width = 480
        self.fps = 10

        self.bridge = CvBridge()
        self.pubstr = "/shadowsense/is_touched"
        self.listeningto = "/shadowsense/camera/raw"
        rospy.init_node("datarecorder", anonymous=True)
        
        self.mode = "notouch"
        self.touchDirectory = "trainingdata/touch"
        self.noTouchDirectory="trainingdata/no_touch"
        self.count = 0

    def listen(self):
        rospy.Subscriber(self.listeningto, Image, self.run)
        rospy.spin()

    def run(self, image):
        self.count += 1
        if self.count %8 !=0:
                return
        current_datetime = datetime.datetime.now()
        cv_image = self.bridge.imgmsg_to_cv2(image, "bgr8")
        path = self.touchDirectory if self.mode == "touch" else self.noTouchDirectory
        filename = "{}/frame{}.jpg".format(path, current_datetime.strftime("%Y%m%d_%H%M%S"))
        print("saved image ",filename)
        cv2.imwrite(filename, cv_image)

if __name__ == '__main__':
    camera = Camera()
    r = rospy.Rate(1)

    camera.listen()
