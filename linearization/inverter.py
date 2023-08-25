import rospy
from geometry_msgs.msg import Twist


rospy.init_node('inverter', anonymous=True)
pub = rospy.Publisher("/controller/cmd_vel_inverted", Twist, queue_size=1)	
rate = rospy.Rate(10)

def talker(stuff:Twist):

	if stuff.linear.x < 0:
		stuff.angular.y *= -1
		
	sstr = f"inverting to x: {stuff.linear.x} y:{stuff.angular.y}"
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

