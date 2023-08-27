Notes to use map and localization with Jackal

Communicating with the jackal
SSH into the jackal
Jackal5: ssh administrator@199.168.1.25
Jackal7 (ASL): ssh administrator@199.168.1.27
Jackal7(ATT-WIFI-h4cp): ssh administrator@192.168.1.57
Jackal5(ATT-WIFI-h4cp): ssh administrator@192.168.1.44
Jackal3(ATT-WIFI-h4cp): ssh administrator@192.168.1.61
ATT Wifi pass: SkyNet2!
Password: clearpath (or check confluence)
Setup an external machine (If you want to send commands or communicate with jackal remotely. Not necessary for mapping)
Create a file named “remote-jackal.sh”
In the file add the following lines,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
export ROS_MASTER_URI=http://jackal5:11311  # Jackal's hostname
export ROS_IP=199.168.1.170               # Your laptop's wireless IP

Get external machine IP with hostname - I
Source the newly created file with source remote-jackal.sh
Check if you can echo topics. If not you may have to match the host with the ip
To add run sudo nano /etc/hosts
Add jackal IP to list of hosts 199.168.1.25	jackal5
Mapping
Launch the velodyne
Terminal 1: roslaunch velodyne_pointcloud VLP16_points.launch
To map
Terminal 2: roslaunch jackal_navigation gmapping_demo.launch scan_topic:=/scan
Drive around slowly and map the area
Terminal 3: rosrun map_server map_saver -f labmap
labmap is the name of the map file and yaml that will be created in whatever directory you are in
To view the map in progress: rosshow /map #WARNING: rosshow sometimes kills the wifi connection
To save the map on the external machine run two commands:
scp administrator@192.168.1.44:/home/administrator/rhodes.pgm rhodes.pgm
scp administrator@199.168.1.25:/home/administrator/labmap.yaml labmap.yaml
administrator@192.168.1.57:/home/administrator/nri_workspace/src/safety_switch.py safety_switch.py

To view on the external machine run: roslaunch jackal_viz view_robot.launch config:=gmapping 
This is working for me but its not really needed
View map on matlab (if graphics problem: matlab -softwareopengl)
Here you can make a line segment map and choose waypoints
Tips for mapping:
Jackal5 will sometimes turn off after a random time. Maybe 20-30 minutes. Not sure why
Be careful of loop closures. Play with the parameters to get something that looks good
People passing by seems to be ok. I would try and constantly move and stay further than the clipping range (5m by default)
Places where the map is hardcoded and should change after remapping
Localization run command (see below)
Specification uses the walls, waypoints in runEvBasedSTL.py
Human pose projection in cleaner.py

Localization
Drive to the origin of your map. Reboot.
Launch the velodyne
Terminal 1: roslaunch velodyne_pointcloud VLP16_points.launch
To map
Terminal 2: roslaunch jackal_navigation amcl_demo.launch map_file:=/home/administrator/rhd3_withoutbox_map6.yaml scan_topic:=/scan
For Upson 5th floor, use full_corridor_first_pass. Issue: The origin for this map is inside of the room, but we want to start in the hallway.
For Rhodes 3rd floor, use rhodesFinal. David says this one is not great, so we should remap.
For Rhodes 3rd floor with added boxes, use rhodes_3rd_boxes. David says this one is not great, so we should remap.
Note: It seems possible to start from not the origin, but the default initial pose is (0,0) 0 yaw
To see pose estimate,
Terminal 3 (amcl global estimate): rosrun tf tf_echo map base_link
Terminal 4 (jackal dead reckoning): rosrun tf tf_echo odom base_link
Topics to record with rosbag record <list of topics below>
/tf
/tf_static
/scan
/odometry/filtered
/jackal_velocity_controller/cmd_vel

Running the MK UWB Tracker
Navigate to the PC Shell folder and run the tracking script
cd ~/mk_uwb/Kit\ SR150_040\ Ext\ pack\ -\ USB\ v3.6/Software/MK\ UWB\ PC\ Shell/MK\ UWB\ PC\ Shell\ v1.1.0/
python3 track_next_device_ros.py /dev/ttyUSB0
Relevant lines of code if you want to modify things
Topic name: pc_shell/device_tracker_ros.py, end of the constructor. Topic name is currently /uwb/relative_tag_location
Pose computation: pc_shell/device_tracker_ros.py, in method rng_aoa_to_tf_stamp. Currently puts the distance as x coordinate, 0 as y coordinate
Code is in this private repo (link). Contact amv78@cornell.edu for access.

Running the Human Tracking
Visualize:
rviz -d ~/Documents/nir_project/humandetect.rviz

Running the Zed camera ROS node
SSh in and, in separate terminals, run
roslaunch zed_wrapper zed.launch
rosshow /zed/zed_node/left/image_rect_color
For an example ROS node that listens to an image and outputs a string, in separate terminals run
python3 ~/touch_sense/image_republisher.py
rostopic echo /zed_img_shape


Running the specification
Find the asl-laptop-1 and login
Username: David
Pass: ASLAdmin!
Run the localization on the robot (see above)
The code for running specifications is in the this repo: https://github.com/davidgundana/Event-based-STL.git
In a new terminal on the local machine, setup the environment and connect to Jackal5
export ROS_MASTER_URI=http://192.168.1.44:11311
conda activate nri
source ~/Documents/nir_project/masterOnJackel.bash
In the same terminal run the specification
cd ~/catkin_ws/src/Event-based-STL/FinalPackage
python3 runEvBasedSTL.py





For Claire: Record all of the sensor data on the jackal
Launch camera
cd ~/catkin_ws/src/zed-ros-wrapper/zed_wrapper/launch
roslaunch zed2.launch
To verify that this works, find the topic name with ‘rostopic list’ run ‘rosshow <topic_name>’ 
/zed2/zed_node/rgb/image_rect_color
/zed2/zed_node/depth/depth_registered
‘rosshow /zed2/zed_node/rgb/image_rect_color’
Launch the velodyne: roslaunch velodyne_pointcloud VLP16_points.launch
rosshow /scan
Topics to record with rosbag record <list of topics below>
/tf
/tf_static
/zed2/zed_node/rgb/image_rect_color
/zed2/zed_node/depth/depth_registered
/scan
/odometry/filtered
/jackal_velocity_controller/cmd_vel








To Run Event-based STL Code
Clone repo
Create a virtual environment inside FinalPackage using conda (Easiest way to install spot on windows and ubuntu): 
Follow this: https://github.com/RoboStack/ros-noetic
Old Nav

   <!-- Process a scan each time the robot translates this far  -->
	<param name="linearUpdate" value="0.1"/>

	<!-- Process a scan each time the robot rotates this far  -->
	<param name="angularUpdate" value="0.05"/>

	<param name="temporalUpdate" value="-1.0"/>
	<param name="resampleThreshold" value="0.5"/>

	<!-- Number of particles in the filter. default 30    	-->
	<param name="particles" value="10"/>








To change audio output device/sink:
pacmd set-default-sink alsa_output.pci-0000_01_00.1.hdmi-stereo-extra1

import pyttsx3
tts = pyttsx3.init()

def say(text):
     tts.say(text)
     tts.runAndWait()
 
say("test")



Running the GoPro
Turning on/ off: Press the button in the front for about 5 seconds

Start/stop the recording: Click the button on the top once

Connecting to the phone: Make sure that the GoPro is off then press the front button for about 10 seconds and find the device on the Quilk app. 
If this doesn’t work, manually set up the go pro to the pairing mode using the following instructions.
Turn on the GoPro
Click on the front button twice until the screen said Preferences
Click on the top button twice until the screen said Pairing
Click the front button once to enter the Pairing mode
On the Quilk side, Go to ->GoPro then hit the add button on the top left corner to find the device. 
Note: if it ask to select a Camera, choose HERO11 Black Mini



Things to run for leading case:
Localization
ssh into Jackal 7:
Open 3 terminals:Launch the velodyne ssh administrator@192.168.1.57


Terminal 1: roslaunch velodyne_pointcloud VLP16_points.launch
Using the map 
Terminal 2:roslaunch jackal_navigation amcl_demo.launch map_file:=/home/administrator/rhd3_fullmap_1.yaml scan_topic:=/scan
roslaunch jackal_navigation amcl_demo.launch map_file:=/home/administrator/rhd3_withoutbox_map6.yaml scan_topic:=/scan
To read robot’s current location estimation
Terminal 3: rosrun tf tf_echo /map /base_link

Projector
ssh into Jackal 7:
Open new terminal: ssh administrator@192.168.1.57
Run the python script:
  python3 subsciber_test2.py
Safety switch
ssh into Jackal 7:
Open new terminal: ssh administrator@192.168.1.57
Run the python script:
cd nri_workspace/src/
python3 safety_switch.py
Rosbag record
ssh into Jackal 7:
Open 3 terminal: ssh administrator@192.168.1.57
Run the rosbag record command with the file you want to record:
rosbag record /cmd_vel /controller/cmd_vel /scan /tf /joy_teleop/cmd_vel
To save the rosbag on the local machine instead of Jackal, run the following 2 lines instead of ssh into the Jackal.
conda activate nri
source ~/Documents/nir_project/masterOnJackel.bash
Specification 
conda activate nri
source ~/Documents/nir_project/masterOnJackel.bash
cd ~/catkin_ws/src/Event-based-STL/FinalPackage
python3 runEvBasedSTL.py
Before 40 degree After about 13 mins with all the human detection running, the temperature was around 62 degree

Things to run for following case:
***Run the Localization First***
Running Human Detection
ssh into Jackal 7:
Open new terminal: ssh administrator@192.168.1.57
Go to corresponding directory:
cd /home/administrator/nri_workspace/
Go to Byobu:
Byobu
Split into 4 terminal: Ctrl+F2 to split screen vertically, Shift + F2 to split screen horizontally
In each terminal, setup the workspace 
source devel/setup.bash
Terminal 1:
Run the pixy cam node: rosrun ros_pixy2_block ros_pixy2_block_node
Terminal 2:
Run theUWB node: rosrun ros_uwb track_next_device_ros /dev/ttyUSB0
Terminal 3: 
Run the Human estimation filter: rosrun human_pose_est human_pose_est_node
Visualizing Human Detection on Rviz
conda activate nri
source ~/Documents/nir_project/masterOnJackel.bash
cd Documents/nir_project/
rviz -d humandetect.rviz


***Run everything that we needed to run for leading case***







