import rospy
from std_msgs.msg import Bool, Int64
from geometry_msgs.msg import PoseStamped, Point

class SS():
    def __init__(self, end:list):
        self.publish_topic = "/shadowsense/is_touched"
        self.rawpub = rospy.Publisher(self.publish_topic, Int64, queue_size=10)
        self.endpoint = Point()
        self.endpoint.x = end[0]
        self.endpoint.y = end[1]
        self.endpoint.z = end[2]

    def talk(self):
        d = Bool()
        d.data = True
        self.rawpub.Publish(d)
        

if __name__ == '__main__':
    rospy.init_node('SS_node')
    ss = SS()
    r = rospy.Rate(10)
    ss.talk()
