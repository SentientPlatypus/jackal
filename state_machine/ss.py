import rospy
from std_msgs.msg import Bool, Int64
from geometry_msgs.msg import PoseStamped, Point

class SS():
    def __init__(self):
        self.publish_topic = "/shadowsense/is_touched"
        self.rawpub = rospy.Publisher(self.publish_topic, Bool, queue_size=10)

    def talk(self):
        print("speaking")
        d = Bool()
        d.data = True
        self.rawpub.publish(d)


if __name__ == '__main__':
    rospy.init_node('SS_node')
    ss = SS()
    r = rospy.Rate(10)
    while not rospy.is_shutdown():
        ss.talk()
        r.sleep()
