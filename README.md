# tesroomba
TesRoomba Project

# Tools

Make sure you have packages from tutorials on ros wiki downloaded (turtlebot_description, turtlebot_gazebo, etc.)

These should be downloaded from lab4 already. Here they are again:

---
**sudo apt-get install ros-kinetic-gmapping
ros-kinetic-turtlebot-gazebosudo apt-get install 
ros-kinetic-turtlebot-simulatorsudo apt-get install 
ros-kinetic-turtlebot-teleopsudo apt-get install 
ros-kinetic-turtlebot-rviz-launchers**

---


For orbslam2 submodule, use https://github.com/appliedAI-Initiative/orb_slam_2_ros
**NOTE: we're no longer using orbslam2 since it's a feature based slam.**

For rtabmap_ros (the slam algorithm we're using), look here: http://wiki.ros.org/rtabmap_ros

To download octomap, use https://github.com/OctoMap/octomap

You will need to download sensor plugin via **sudo apt-get install libgazebo7-dev**, which will be used for our custom cameras in gazebo.

We may also need to use this for rectifing our images. Probably more useful for the hardware version of our project.
https://github.com/ros-perception/image_pipeline



---

To edit the floorplan, generate a new .sdf file and add the directory to it in place of my_world.sdf. my_world.sdf is just the floorplan I first generated. .world files also work too.

To create our own sensors (like cameras) reference: http://gazebosim.org/tutorials?tut=ros_gzplugins


# How to run and progress:

To run the current floor plan, after *source/devel/setup.bash* and the editing the corresponding files (look below), run

```
export  TURTLEBOT_3D_SENSOR=custom

roslaunch jump_start turtlebot_world.launch world_file:=$(rospack find jump_start)/worlds/my_world.sdf
```

To change the topics being published, use a remap.
To change the sensors being used, instead of custom, put r200, kinect, etc. To check which ones are supported, look at the .launch files.

camera1 is the left camera.
camera2 is the right camera

## 12/6/20 

### Update

The floorplan runs by just calling the same commands as above. Currently waiting on a more "touched up" floorplan, but that's an easy fix. We just have to change the world_file. Orb_slam2_ros is also up and running now. Just run ***roslaunch jump_start orb_slam2_ros.launch*** and ***roslaunch jump_start gmapping.launch***. The orb slam launch file is based off of the r200 launch file that comes with orb_slam2_ros. We are also using a gmapping launch for localization in the space as we need this for orb slam 2 to work properly as of right now. This is because gmapping provides the transformation between the /odom frame and /camera_link frame. Not sure if gmapping is also necessary, but it's fine for now. 

To get an occupany grid going, in addition to running the above, run ***roslaunch jump_start octomap.launch***. To see it in rviz, use markerarray. **NOTE THAT the octomap isn't working right now as Alex needs to fix something.**

To move turtlebot, run ***roslaunch turtlebot_teleop keyboard_teleop.launch --screen***.

– Alex

#### Next:

Since we have a somewhat occupany grid working as you can observe from octomap, we just need to condense it down to 2D. I believe that there's a "filter" for this using octomap; I saw something like that somewhere in roswiki. Now, we can also start implementing a controller and a neural network for detection. I'm not sure where hardware is at this point. It's sort of on the backburner for me (Alex).

## 12/7/20 

### Update

We believe. Time is running out. Where's the avatar?
So the issue with orb_slam2 is that it's a feature extractor, which means it doesn't do the full on slam that a laser does. Working on getting that fixed. For cameras, we now use ***stereo_image_proc*** because it rectifies images and makes our lives a whole lot easier since it publishes a point cloud and rectified images. However, the pointcloud it published is weird since optical cameras have a different notion of a frame (ie. the z axis points into the plane of the image). Thus, I hacked the frames such that oleft is the "normal" orientation of the left camera, which "left" is oleft rotated by rpy = -90, 0, -90 in degrees because images are weird like that.

#### Next:

I will be trying different slam algorithms tonight and try to get a controller up and running. We're also using a turtlebot instead of a actual roomba, which might be bad? I can't get a roomba to work in simulation unfortunately. It's stupidly difficult for no reason.

## 12/8/20

### Update

So we've decided to go with **rtabmap_ros** since orb_slam2 was just not cutting it for some reason. We wrote a wrapper for our camera around the turtlebot and now it's working pretty well. 

As far as commands go:

```
export  TURTLEBOT_3D_SENSOR=custom

roslaunch jump_start turtlebot_world.launch world_file:=$(rospack find jump_start)/worlds/my_world.sdf
```
in one terminal for world launching. 

```
roslaunch jump_start image_proc.launch
```
for image processing/rectification.
```
roslaunch rtabmap_ros stereo_mapping.launch.
```

Teleoperation is the same, and you'll also have to modify some of the parameters in **stereo_mapping.launch**.

Here are the parameters in **stereo_mapping.launch**:

```
  <arg name="rtabmapviz"              default="true" />
  <arg name="rviz"                    default="false" />

  <!-- Localization-only mode -->
  <arg name="localization"            default="false"/>

  <!-- Corresponding config files -->
  <arg name="rtabmapviz_cfg"          default="$(find rtabmap_ros)/launch/config/rgbd_gui.ini" />
  <arg name="rviz_cfg"                default="$(find rtabmap_ros)/launch/config/rgbd.rviz" />

  <arg name="frame_id"                default="left"/>     <!-- Fixed frame id, you may set "base_link" or "base_footprint" if they are published -->
  <arg name="database_path"           default="~/.ros/rtabmap.db"/>
  <arg name="rtabmap_args"            default=""/>   <!-- delete_db_on_start, udebug -->
  <arg name="launch_prefix"           default=""/>
  <arg name="approx_sync"             default="true"/>         <!-- if timestamps of the input topics are not synchronized -->

  <arg name="stereo_namespace"        default=""/>
  <arg name="left_image_topic"        default="/stereo/camera/left/image_rect_color" />
  <arg name="right_image_topic"       default="/stereo/camera/right/image_rect" />      <!-- using grayscale image for efficiency -->
  <arg name="left_camera_info_topic"  default="/stereo/camera/left/camera_info" />
  <arg name="right_camera_info_topic" default="/stereo/camera/right/camera_info" />
  <arg name="compressed"              default="false"/>

  <arg name="subscribe_scan"          default="false"/>         <!-- Assuming 2D scan if set, rtabmap will do 3DoF mapping instead of 6DoF -->
  <arg name="scan_topic"              default="/scan"/>

  <arg name="subscribe_scan_cloud"    default="false"/>         <!-- Assuming 3D scan if set -->
  <arg name="scan_cloud_topic"        default="/scan_cloud"/>

  <arg name="visual_odometry"         default="false"/>          <!-- Generate visual odometry -->
  <arg name="odom_topic"              default="/odom"/>         <!-- Odometry topic used if visual_odometry is false -->
  <arg name="odom_frame_id"           default="/odom"/>              <!-- If set, TF is used to get odometry instead of the topic -->

  <arg name="namespace"               default="rtabmap"/>
  <arg name="wait_for_transform"      default="0.2"/>
  <arg name="queue_size"              default="100"/>
  ```










