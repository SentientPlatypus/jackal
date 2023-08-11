import rospy
from geometry_msgs.msg import TransformStamped
from roadmap import RoadMap

rd = RoadMap("rhd3_map_3_walls.txt", "rhd3_map_3_waypoints.txt")
rospy.init_node('listener', anonymous=True)
pub = rospy.Publisher("newer", TransformStamped, queue_size=1)	
rate = rospy.Rate(10)

def talker(stuff:TransformStamped):

	projection = rd.project([stuff.transform.translation.x, stuff.transform.translation.y])
	stuff.header.frame_id = "THIS IS PROJECTED"
	stuff.transform.translation.x = projection[0]
	stuff.transform.translation.y = projection[1]
	sstr = "repeating"
	rospy.loginfo(sstr)
	pub.publish(stuff)
	rate.sleep()
		
def callback(data):
	rospy.loginfo(rospy.get_caller_id() + f"I heard {data}")
	talker(data)

def listener():
	rate.sleep()
	rospy.Subscriber("chatter", TransformStamped, callback)
	rospy.spin()
	
	
def periodic():
	listener()

if __name__ == "__main__":
	periodic()

