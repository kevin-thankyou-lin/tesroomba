# tesroomba
TesRoomba Project


For orbslam2 submodule, use https://github.com/appliedAI-Initiative/orb_slam_2_ros

# How to run and progress:

To run the current floor plan, after *source/devel/setup.bash*, run 

---
***roslaunch turtlebot_gazebo turtlebot_world.launchworld_file:=$(rospack find lab4_starter)/worlds/my_world.sdf***

---
To edit the floorplan, generate a new .sdf file and add the directory to it in place of my_world.sdf. my_world.sdf is just the floorplan I first generated. .world files also work too.

