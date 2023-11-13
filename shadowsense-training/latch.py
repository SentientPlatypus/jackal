#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
#from sensor_msgs.msg import LaserScan
import math

was_touched = False
pub = rospy.Publisher('/shadowsense/was_touched', Bool, queue_size=10) #initialize the publisher

#decide the axis
def callback_classifier(data):
    global was_touched
    if (data.data):
        was_touched = True
    pub.publish(was_touched)


def latch():
    rospy.init_node('latch', anonymous=True)
    rospy.Subscriber("/shadowsense/is_touched", Bool, callback_classifier)
    rospy.spin()


if __name__ == '__main__':
    latch()
  
