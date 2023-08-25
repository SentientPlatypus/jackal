import rospy
from geometry_msgs.msg import TransformStamped


def callback(data):
	rospy.loginfo(rospy.get_caller_id() + f"I heard {data}")

def listener():
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber("newer", TransformStamped, callback)
	rospy.spin()


if __name__ == "__main__":
	listener()

