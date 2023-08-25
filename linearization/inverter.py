import rospy
from geometry_msgs.msg import Twist
from roadmap import RoadMap


rospy.init_node('inverter', anonymous=True)
pub = rospy.Publisher("/controller/cmd_vel_inverted", Twist, queue_size=1)	
rate = rospy.Rate(10)

def talker(stuff:Twist):
	stuff.header.frame_id = "THIS IS INVERTED"
	

	if stuff.linear.x < 0:
		stuff.angular.y *= 1
		
	sstr = "inverting"
	rospy.loginfo(sstr)
	pub.publish(stuff)
	rate.sleep()
		
def callback(data):
	rospy.loginfo(rospy.get_caller_id() + f"I heard {data}")
	talker(data)

def listener():
	rate.sleep()
	rospy.Subscriber("/controller/cmd_vel", Twist, callback)
	rospy.spin()
	
	
def periodic():
	listener()

if __name__ == "__main__":
	periodic()

