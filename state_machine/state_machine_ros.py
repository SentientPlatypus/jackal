import rospy
from cv_bridge import CvBridge
from std_msgs.msg import Bool, Int
from geometry_msgs.msg import PoseStamped, Point

class State():
    FOLLOW = 0
    LEAD = 1
    DONE = 2
    STUCH = 4

class StateMachine():
    def __init__(self, end:list):
        self.state = State.FOLLOW
        self.publish_topic = "/statemachine/state"
        self.rawpub = rospy.Publisher(self.publish_topic, Int, queue_size=10)
        
        self.message_dispatch = {
            State.FOLLOW: self.on_follow,
            State.LEAD: self.on_lead
        }
        self.endpoint = Point()
        self.endpoint.x = end[0]
        self.endpoint.y = end[1]
        self.endpoint.z = end[2]

    def listen(self):
        rospy.Subscriber("/shadowsense/is_touched", Bool, self.message_dispatcher)
        rospy.Subscriber("/amcl_pose", PoseStamped, self.message_dispatcher)  # Replace with your actual topic

        rospy.spin()

    def on_follow(self, boolean):
        if boolean.data:
            self.state = State.LEAD
            self.publish_state()
    
    def on_lead(self, pose):

        if pose.pose.position == self.endpoint:
            self.state = State.DONE
            self.publish_state()

    def publish_state(self):
        state_msg = Int()
        state_msg.data = self.state
        self.rawpub.publish(state_msg)

    def message_dispatcher(self, msg):
        if self.state in self.message_dispatch:
            self.message_dispatch[self.state](msg)

if __name__ == '__main__':
    rospy.init_node('state_machine_node')
    statemachine = StateMachine([18.4, -38.91, 0])
    r = rospy.Rate(10)
    statemachine.listen()
