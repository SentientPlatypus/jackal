# Notes to use map and localization with Jackal


### Communicating with the Jackal
1. SSH into the jackal
	* `Jackal5: ssh administrator@199.168.1.25`
	* `Jackal7 (ASL): ssh administrator@199.168.1.27`
	* `Jackal7(ATT-WIFI-h4cp): ssh administrator@192.168.1.57`
	* `Jackal5(ATT-WIFI-h4cp): ssh administrator@192.168.1.44`
	* `Jackal3(ATT-WIFI-h4cp): ssh administrator@192.168.1.61`
	* ATT Wifi pass: `SkyNet2!`
	SSH Password: `clearpath` (or check confluence)

2. Setup an external machine (If you want to send commands or communicate with jackal remotely. Not necessary for mapping)
	* Create a file named `remote-jackal.sh`
	* In the file add the following lines
	```sh
	export ROS_MASTER_URI=http://jackal5:11311  # Jackal's hostname
	export ROS_IP=199.168.1.170               # Your laptop's wireless IP
	```
	* Get external machine IP with `hostname - I`
	* Source the newly created file with `source remote-jackal.sh`
	* Check if you can echo topics. If not you may have to match the host with the ip
		- To add run `sudo nano /etc/hosts`
		- Add jackal IP to list of hosts `199.168.1.25	jackal5`

### Mapping
1. Launch the velodyne
	* Terminal 1: `roslaunch velodyne_pointcloud VLP16_points.launch`
2. To map
	* Terminal 2: `roslaunch jackal_navigation gmapping_demo.launch scan_topic:=/scan`
	* Drive around slowly and map the area
	* Terminal 3: `rosrun map_server map_saver -f labmap`
		- labmap is the name of the map file and yaml that will be created in whatever directory you are in
	* To view the map in progress: rosshow /map #WARNING: rosshow sometimes kills the wifi connection
3. To save the map on the external machine run two commands:
```sh
scp administrator@192.168.1.44:/home/administrator/rhodes.pgm rhodes.pgm
scp administrator@199.168.1.25:/home/administrator/labmap.yaml labmap.yaml
administrator@192.168.1.57:/home/administrator/nri_workspace/src/safety_switch.py safety_switch.py
```

	* To view on the external machine run: `roslaunch jackal_viz view_robot.launch config:=gmapping `
		- This is working for me but its not really needed
	* View map on matlab (if graphics problem: `matlab -softwareopengl`) Here you can make a line segment map and choose waypoints.

4. Tips for mapping:
	* Jackal5 will sometimes turn off after a random time. Maybe 20-30 minutes. Not sure why
	* Be careful of loop closures. Play with the parameters to get something that looks good
	* People passing by seems to be ok. I would try and constantly move and stay further than the clipping range (5m by default)
5. Places where the map is hardcoded and should change after remapping
	* Localization run command (see below)
	* Specification uses the walls, waypoints in runEvBasedSTL.py
	* Human pose projection in cleaner.py

### Localization
1. Drive to the origin of your map. Reboot.
2. Launch the velodyne
	* Terminal 1: `roslaunch velodyne_pointcloud VLP16_points.launch`
3. To map
	* Terminal 2: `roslaunch jackal_navigation amcl_demo.launch map_file:=/home/administrator/rhd3_withoutbox_map6.yaml scan_topic:=/scan`
	* For Upson 5th floor, use full_corridor_first_pass. Issue: The origin for this map is inside of the room, but we want to start in the hallway.
	* For Rhodes 3rd floor, use rhodesFinal. David says this one is not great, so we should remap.
	* For Rhodes 3rd floor with added boxes, use rhodes_3rd_boxes. David says this one is not great, so we should remap.
	* Note: It seems possible to start from not the origin, but the default initial pose is (0,0) 0 yaw
4. To see pose estimate,
	* Terminal 3 (amcl global estimate): `rosrun tf tf_echo map base_link`
	* Terminal 4 (jackal dead reckoning): `rosrun tf tf_echo odom base_link`
5. Topics to record with rosbag record:
```sh
/tf
/tf_static
/scan
/odometry/filtered
/jackal_velocity_controller/cmd_vel
```

### Running the MK UWB Tracker
1. Navigate to the PC Shell folder and run the tracking script
	* `cd ~/mk_uwb/Kit\ SR150_040\ Ext\ pack\ -\ USB\ v3.6/Software/MK\ UWB\ PC\ Shell/MK\ UWB\ PC\ Shell\ v1.1.0/`
	* `python3 track_next_device_ros.py /dev/ttyUSB0`
2. Relevant lines of code if you want to modify things
	* Topic name: pc_shell/device_tracker_ros.py, end of the constructor. Topic name is currently /uwb/relative_tag_location
	* Pose computation: pc_shell/device_tracker_ros.py, in method rng_aoa_to_tf_stamp. Currently puts the distance as x coordinate, 0 as y coordinate
Code is in [this](https://github.com/violetteavi/mk_uwb_tracker/) private repo=. Contact amv78@cornell.edu for access.

Running the Human Tracking
Visualize:
rviz -d ~/Documents/nir_project/humandetect.rviz


### Running the Zed camera ROS node
1. SSh in and, in separate terminals, run
```sh
roslaunch zed_wrapper zed.launch
```
```sh
rosshow /zed/zed_node/left/image_rect_color
```
2. For an example ROS node that listens to an image and outputs a string, in separate terminals run

```sh
python3 ~/touch_sense/image_republisher.py
```
```sh
rostopic echo /zed_img_shape
```







