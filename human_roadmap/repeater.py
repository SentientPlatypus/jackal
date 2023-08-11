import rospy
from geometry_msgs.msg import TransformStamped


def talker(stuff):
	pub = rospy.Publisher("newer", TransformStamped, queue_size=1)	
	rate = rospy.Rate(10)
	sstr = "repeating"
	rospy.loginfo(sstr)
	pub.publish(stuff)
	rate.sleep()
		
def callback(data):
	rospy.loginfo(rospy.get_caller_id() + f"I heard {data}")
	talker(data)

def listener():
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber("chatter", TransformStamped, callback)
	rospy.spin()
	
	
def periodic():
	listener()

if __name__ == "__main__":
	periodic()

