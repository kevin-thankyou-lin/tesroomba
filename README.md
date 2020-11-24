# tesroomba
TesRoomba Project


For orbslam2 submodule, use https://github.com/appliedAI-Initiative/orb_slam_2_ros

# How to run and progress:

To run the current floor plan, after *source/devel/setup.bash*, run 

---
***roslaunch turtlebot_gazebo turtlebot_world.launch world_file:=$(rospack find lab4_starter)/worlds/my_world.sdf***

---
To edit the floorplan, generate a new .sdf file and add the directory to it in place of my_world.sdf. my_world.sdf is just the floorplan I first generated. .world files also work too.

To create our own camera sensors reference: http://gazebosim.org/tutorials?tut=ros_gzplugins

Alex's current implementation: 

In turtlebot_gazebo.urdf.xacro, which is located in library turtlebot_gazebo: 
---
<?xml version="1.0"?>
<robot name="turtlebot_gazebo" xmlns:xacro="http://ros.org/wiki/xacro">
  <!-- Microsoft Kinect / ASUS Xtion PRO Live for simulation -->
  <xacro:macro name="turtlebot_sim_3dsensor">
    <gazebo reference="camera_link">
      <sensor type="camera" name="camera">
        <update_rate>30.0</update_rate>
         <camera name="head">
           <horizontal_fov>1.3962634</horizontal_fov>
           <image>
             <width>800</width>
             <height>800</height>
             <format>R8G8B8</format>
           </image>
           <clip>
             <near>0.02</near>
             <far>300</far>
           </clip>
           <noise>
             <type>gaussian</type>
             <!-- Noise is sampled independently per pixel on each frame.
                  That pixel's noise value is added to each of its color
                  channels, which at that point lie in the range [0,1]. -->
             <mean>0.0</mean>
             <stddev>0.007</stddev>
           </noise>
         </camera>
        <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
          <cameraName>camera</cameraName>
          <alwaysOn>true</alwaysOn>
          <updateRate>0.0</updateRate>
          <cameraName>rrbot/camera1</cameraName>
          <imageTopicName>image_raw</imageTopicName>
          <cameraInfoTopicName>camera_info</cameraInfoTopicName>
          <frameName>camera_link</frameName>
          <hackBaseline>0.07</hackBaseline>
          <distortionK1>0.0</distortionK1>
          <distortionK2>0.0</distortionK2>
          <distortionK3>0.0</distortionK3>
          <distortionT1>0.0</distortionT1>
          <distortionT2>0.0</distortionT2>
        </plugin>
      </sensor>
    </gazebo>
  </xacro:macro>
</robot>

---

You will also need to download plugins via sudo apt-get install libgazebo7-dev

You'll also need to include a turtlebot.gazebo file with the following:

---
<robot>
  <!-- camera -->
  <gazebo reference="camera_link">
    <sensor type="camera" name="camera1">
      <update_rate>30.0</update_rate>
      <camera name="head">
        <horizontal_fov>1.3962634</horizontal_fov>
        <image>
          <width>800</width>
          <height>800</height>
          <format>R8G8B8</format>
        </image>
        <clip>
          <near>0.02</near>
          <far>300</far>
        </clip>
        <noise>
          <type>gaussian</type>
          <!-- Noise is sampled independently per pixel on each frame.
               That pixel's noise value is added to each of its color
               channels, which at that point lie in the range [0,1]. -->
          <mean>0.0</mean>
          <stddev>0.007</stddev>
        </noise>
      </camera>
      <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
        <alwaysOn>true</alwaysOn>
        <updateRate>0.0</updateRate>
        <cameraName>rrbot/camera1</cameraName>
        <imageTopicName>image_raw</imageTopicName>
        <cameraInfoTopicName>camera_info</cameraInfoTopicName>
        <frameName>camera_link</frameName>
        <hackBaseline>0.07</hackBaseline>
        <distortionK1>0.0</distortionK1>
        <distortionK2>0.0</distortionK2>
        <distortionK3>0.0</distortionK3>
        <distortionT1>0.0</distortionT1>
        <distortionT2>0.0</distortionT2>
      </plugin>
    </sensor>
  </gazebo>

</robot>


---

Kinect.urdf.xacro will have the following:

---
<?xml version="1.0"?>
<robot name="sensor_kinect" xmlns:xacro="http://ros.org/wiki/xacro">
  <xacro:include filename="$(find turtlebot_description)/urdf/turtlebot_gazebo.urdf.xacro"/>
  <xacro:include filename="$(find turtlebot_description)/urdf/turtlebot_properties.urdf.xacro"/>

  <xacro:property name="camera_link" value="0.05" /> <!-- Size of square 'camera' box -->
  <xacro:property name="kinect_cam_py" value="-0.0125"/>
  <!-- Parameterised in part by the values in turtlebot_properties.urdf.xacro -->
  <xacro:macro name="sensor_kinect" params="parent">
    <joint name="camera_rgb_joint" type="fixed">
      <origin xyz="${cam_px} ${kinect_cam_py} ${cam_pz}" rpy="${cam_or} ${cam_op} ${cam_oy}"/>
      <parent link="${parent}"/>
      <child link="camera_rgb_frame" />
    </joint>
    <link name="camera_rgb_frame"/>

    <joint name="camera_rgb_optical_joint" type="fixed">
      <origin xyz="0 0 0" rpy="${-M_PI/2} 0 ${-M_PI/2}" />
      <parent link="camera_rgb_frame" />
      <child link="camera_rgb_optical_frame" />
    </joint>
    <link name="camera_rgb_optical_frame"/>

    <joint name="camera_joint" type="fixed">
      <origin xyz="-0.031 ${-kinect_cam_py} -0.016" rpy="0 0 0"/>
      <parent link="camera_rgb_frame"/>
      <child link="camera_link"/>
    </joint>
      <link name="camera_link">
      <visual>
       <origin xyz="0 0 0" rpy="0 0 ${M_PI/2}"/>
       <geometry>
         <box size="${camera_link} ${camera_link} ${camera_link}"/>
         <material name="red"/>
       </geometry>

      </visual>

  	  <collision>
        <origin xyz="0.0 0.0 0.0" rpy="0 0 0"/>
  	    <geometry>
  	      <box size="0.07271 0.27794 0.073"/>
  	    </geometry>
  	  </collision>

      <inertial>
        <mass value="0.564" />
        <origin xyz="0 0 0" />
        <inertia ixx="0.003881243" ixy="0.0" ixz="0.0"
                 iyy="0.000498940" iyz="0.0"
                 izz="0.003879257" />
      </inertial>
    </link>

    <!-- The fixed joints & links below are usually published by static_transformers launched by the OpenNi launch
         files. However, for Gazebo simulation we need them, so we add them here.
         (Hence, don't publish them additionally!) -->

	<!-- Kinect sensor for simulation -->
	<!-- <turtlebot_sim_3dsensor/> -->
  </xacro:macro>
</robot>

---




