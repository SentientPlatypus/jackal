import rospy
from cv_bridge import CvBridge
from std_msgs.msg import Bool, Int64
from geometry_msgs.msg import PoseWithCovarianceStamped, Point
import subprocess
import os

class State():
    FOLLOW = 0
    LEAD = 1
    DONE = 2
    STUCH = 4

class StateMachine():
    def __init__(self, end:list):
        self.state = State.FOLLOW
        self.publish_topic = "/statemachine/state"
        self.rawpub = rospy.Publisher(self.publish_topic, Int64, queue_size=10)
        self.endpoint = Point()
        self.endpoint.x = end[0]
        self.endpoint.y = end[1]
        self.endpoint.z = end[2]
        self.exit_img = "exit.png"
        self.followimg = "follow.png"

        self.viewer = subprocess.Popen(["feh", "-F", self.followimg], env = dict(os.environ,DISPLAY=":0"))


        print("Initialized, current state is " + str(self.state))
        
    def listenpose(self):
        print("listening for pose")
        rospy.Subscriber("/amcl_pose", PoseWithCovarianceStamped, self.on_lead)  # Replace with your actual topic
        rospy.spin()

    def listenshadow(self):
        print("listening for shadowsense")
        rospy.Subscriber("/shadowsense/is_touched", Bool, self.on_follow)
        rospy.spin()

    def on_follow(self, boolean):
        if self.state == State.FOLLOW:
            self.viewer.terminate()
            self.viewer = subprocess.Popen(["feh", "-F", self.followimg], env = dict(os.environ,DISPLAY=":0"))
            if boolean.data:
                self.state = State.LEAD
                self.publish_state()
    
    def on_lead(self, pose):
        if self.state == State.LEAD:
            self.viewer.terminate()
            self.viewer = subprocess.Popen(["feh", "-F", self.exit_img], env = dict(os.environ,DISPLAY=":0"))
            if pose.pose.pose.position == self.endpoint:
                self.state = State.DONE
                self.publish_state()

    def publish_state(self):
        state_msg = Int64()
        state_msg.data = self.state
        self.rawpub.publish(state_msg)
        print("new_state" + str(self.state))


if __name__ == '__main__':
    rospy.init_node('state_machine_node')
    statemachine = StateMachine([18.4, -38.91, 0])
    r = rospy.Rate(10)
    statemachine.listen()
