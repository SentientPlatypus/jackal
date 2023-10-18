import rospy
from std_msgs.msg import Bool, Int64
from geometry_msgs.msg import PoseStamped, Point

class Pos():
    def __init__(self, end:list):
        self.publish_topic = "/amcl_pose"
        self.rawpub = rospy.Publisher(self.publish_topic, Point, queue_size=10)
        self.endpoint = Point()
        self.endpoint.x = end[0]
        self.endpoint.y = end[1]
        self.endpoint.z = end[2]

    def talk(self):
        self.rawpub.publish(self.endpoint)
        rospy.spin()        

if __name__ == '__main__':
    rospy.init_node('Pos_node')
    p = Pos([18.4, -38.91, 0])
    r = rospy.Rate(10)
    p.talk()
