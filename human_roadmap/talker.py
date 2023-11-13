import rospy
from geometry_msgs.msg import TransformStamped


def talker():
	pub = rospy.Publisher("human_with_filter_inertial", TransformStamped, queue_size=1)
	rospy.init_node('talker', anonymous=True)
	rate = rospy.Rate(10)
	while not rospy.is_shutdown():
		t = TransformStamped()
		t.transform.translation.x = 0 #18
		t.transform.translation.y = 0 #-19
		t.transform.rotation.w = 0
		t.header.stamp = rospy.Time.now()
		t.header.frame_id = "map"
		t.child_frame_id = "human_with_filter"
		pub.publish(t)
		rate.sleep()


if __name__ == "__main__":
	talker()


