import rospy
from geometry_msgs.msg import TransformStamped
from std_msgs.msg import Header


def talker():
	pub = rospy.Publisher("chatter", TransformStamped, queue_size=1)
	rospy.init_node('talker', anonymous=True)
	rate = rospy.Rate(10)
	t = TransformStamped()
	#t.header = Header()
	#t.child_frame_id = "hi"
	#t.transform = 
	while not rospy.is_shutdown():
		sstr = "hello"
		rospy.loginfo(sstr)
		pub.publish(t)
		rate.sleep()


if __name__ == "__main__":
	try:
		talker()
	except rospy.ROSInterruptException:
		pass


