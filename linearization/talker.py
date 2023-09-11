import rospy
from geometry_msgs.msg import Twist


def talker():
	pub = rospy.Publisher("/controller/cmd_vel", Twist, queue_size=1)
	rospy.init_node('talker', anonymous=True)
	rate = rospy.Rate(10)
	while not rospy.is_shutdown():
		t = Twist()
		t.linear.x = -.1
		t.angular.z = .1
		pub.publish(t)
		rate.sleep()


if __name__ == "__main__":
	talker()


