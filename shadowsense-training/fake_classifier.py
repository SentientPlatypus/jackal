#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
#from sensor_msgs.msg import LaserScan
import math

touched = False
pub = rospy.Publisher('/shadowsense/is_touched', Bool, queue_size=10) #initialize the publisher

#decide the axis
def callback_joy(data):
    global touched
    if (data.axes[2] < 0.95 and not (data.axes[5]>-0.001 and data.axes[5]<0.001)):
    	touched = True
    	pub.publish(touched)
    else: 
    	touched = False
    	pub.publish(touched)

def false_classifier():
    print("Setting up subscriber...")
    rospy.init_node('false_classifier', anonymous=True)
    rospy.Subscriber("/bluetooth_teleop/joy", Joy, callback_joy)
    print("Spinning...")
    rospy.spin()
    print("Done.")

if __name__ == '__main__':
    false_classifier()
    print("Ran classifier")
