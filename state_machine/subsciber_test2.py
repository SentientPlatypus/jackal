import rospy
from std_msgs.msg import String
import subprocess
import time
import tf
import os
import pyttsx3


if __name__ == '__main__':
    image_file1 = "follow.png"
    image_file2 = "exit.png"
    rospy.init_node('turtle_tf_listener')
    tts = pyttsx3.init()

    listener = tf.TransformListener()
    thres = 0.5

    #turtle_vel = rospy.Publisher('turtle2/cmd_vel', geometry_msgs.msg.Twist,queue_size=1)
    location_found = True
    rate = rospy.Rate(10.0)

    subprocess.Popen(["cp",image_file1,"temp.png"])
    viewer = subprocess.Popen(["feh", "--auto-reload","-R","0.1","-F", "temp.png"], env = dict(os.environ,DISPLAY=":0"))
    def say(text):
     tts.say(text)
     tts.runAndWait()
    say("hello")

    viewer = subprocess.Popen(["feh", "-F", image_file2], env = dict(os.environ,DISPLAY=":0"))
    time.sleep(5)
    viewer.terminate()


    while not rospy.is_shutdown():

        try:
            location_found = True
            (trans,rot) = listener.lookupTransform('map', 'base_link', rospy.Time(0))
            exit_x , exit_y = 18.4, -38.91
            x, y = trans[0], trans[1]
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            location_found = False
            print("location not found!")
            say("not found")
            continue
        # try:
        #     (trans_h,rot_h) = listener.lookupTransform('base_link', 'human', rospy.Time(0))
        # except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        #     continue
        print("location x: ")
        print(x)
    
        if location_found and abs(x - exit_x) < thres and abs(y - exit_y) < thres:
            try:
                print("exit")
                viewer = subprocess.Popen(["feh", "-F", image_file2], env = dict(os.environ,DISPLAY=":0"))
                say("exit_here")
                time.sleep(5)
                viewer.terminate()
            except:
                print("display exit (failed)")
                continue  
            #display here at exit!
        else:
            # try:
            subprocess.Popen(["cp",image_file1,"temp.png"])
            time.sleep(2)
            say("follow_me")
            print("follow")
            #subprocess.Popen(["cp",image_file2,"temp.png"])

            # viewer = subprocess.Popen(["feh", "-F", image_file1], env = dict(os.environ,DISPLAY=":1")) 
            #os.putenv("DISPLAY","1")
            #viewer = subprocess.call("feh -F " + image_file1, shell = True)
            #time.sleep(2)
            viewer.terminate()  
            #display follow me
            # except:
            #     print("display follow me (failed)")
            #     continue

        #make a figure of map
        #draw a dot of x,y

        # angular = 4 * math.atan2(trans[1], trans[0])
        # linear = 0.5 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)
        # cmd = geometry_msgs.msg.Twist()
        # cmd.linear.x = linear
        # cmd.angular.z = angular
        # turtle_vel.publish(cmd)

        rate.sleep()
