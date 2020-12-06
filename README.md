# tesroomba
TesRoomba Project

Make sure you have packages from tutorials on ros wiki downloaded (turtlebot_description, turtlebot_gazebo, etc.)


For orbslam2 submodule, use https://github.com/appliedAI-Initiative/orb_slam_2_ros

To download octomap, use https://github.com/OctoMap/octomap

You will need to download sensor plugin via **sudo apt-get install libgazebo7-dev**

---

To edit the floorplan, generate a new .sdf file and add the directory to it in place of my_world.sdf. my_world.sdf is just the floorplan I first generated. .world files also work too.

To create our own camera sensors reference: http://gazebosim.org/tutorials?tut=ros_gzplugins


# How to run and progress:

To run the current floor plan, after *source/devel/setup.bash* and the editing the corresponding files (look below), run

```
***export  TURTLEBOT_3D_SENSOR=custom***

***roslaunch jump_start turtlebot_world.launch world_file:=$(rospack find jump_start)/worlds/my_world.sdf***
```

To change the topics being published, use a remap.
To change the sensors being used, instead of custom, put r200, kinect, etc.

camera1 is the left camera.
camera2 is the right camera

## 12/6/20 

### Update

The floorplan runs by just calling the same commands as above. Currently waiting on a more "touched up" floorplan, but that's an easy fix. We just have to change the world_file. Orb_slam2_ros is also up and running now. Just run ***roslaunch jump_start orb_slam2_ros.launch*** and ***roslaunch jump_start gmapping.launch***. The orb slam launch file is based off of the r200 launch file that comes with orb_slam2_ros. We are also using a gmapping launch for localization in the space as we need this for orb slam 2 to work properly as of right now. This is because gmapping provides the transformation between the /odom frame and /camera_link frame. Not sure if gmapping is also necessary, but it's fine for now. 

To get an occupany grid going, in addition to running the above, run ***roslaunch jump_start octomap.launch***. To see it in rviz, use markerarray. **NOTE THAT the octomap isn't working right now as Alex needs to fix something.**

– Alex

#### Next:

Since we have a somewhat occupany grid working as you can observe from octomap, we just need to condense it down to 2D. I believe that there's a "filter" for this using octomap; I saw something like that somewhere in roswiki. Now, we can also start implementing a controller and a neural network for detection. I'm not sure where hardware is at this point. It's sort of on the backburner for me (Alex).









