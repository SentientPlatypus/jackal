import rospy
from geometry_msgs.msg import TransformStamped
from human_roadmap.roadmap import RoadMap

rd = RoadMap("/home/david/catkin_ws/src/Event-based-STL/FinalPackage/Maps/rhd3_withoutbox_map6_walls.txt", "/home/david/catkin_ws/src/Event-based-STL/FinalPackage/Maps/rhd3_withoutbox_map6_waypoints.txt")
rospy.init_node('human_pose_cleaner', anonymous=True)
pub = rospy.Publisher("human_with_filter_projected", TransformStamped, queue_size=1)	

def talker(stuff:TransformStamped):
	projection = rd.project([stuff.transform.translation.x, stuff.transform.translation.y])
	stuff.header.frame_id = "map"
	stuff.child_frame_id = "human_on_roadmap"
	stuff.transform.translation.x = projection[0]
	stuff.transform.translation.y = projection[1]
	pub.publish(stuff)
		
def callback(data):
	rospy.loginfo(rospy.get_caller_id() + f"I heard {data}")
	talker(data)

def listener():
	rospy.Subscriber("human_with_filter_inertial", TransformStamped, callback)
	rospy.spin()
	
	
def periodic():
	listener()

if __name__ == "__main__":
	periodic()

