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

To run the current floor plan, after *source/devel/setup.bash* and the editing the corresponding files (look below), run \

```
***export  TURTLEBOT_3D_SENSOR=custom***

***roslaunch turtlebot_gazebo turtlebot_world.launch world_file:=$(rospack find jump_start)/worlds/my_world.sdf***
```

To change the topics being published, use a remap.
To change the sensors being used, instead of custom, put r200, kinect, etc.



