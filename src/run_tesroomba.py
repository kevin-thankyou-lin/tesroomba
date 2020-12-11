# from Collections import deque
from std_msgs.msg import Header
# from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose, Point, Quaternion, Twist, PoseStamped

from nav_msgs.msg import OccupancyGrid
from actionlib_msgs.msg import *
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from occ_grid import OccGrid

import rospy
import tf2_ros
import sys
import tf

import matplotlib.pyplot as plt

WORLD_FRAME = "odom" # world frame is the odom frame - map from moves w.r.t to the move frame!
ROBOT_FRAME = "base_link"

STOPPING_FRONTIER_PTS_NUM = 5
ROTATE_TIME = 0

class TesRoo:
    def __init__(self, angular_vel=0.2):
        self.occ_grid = OccGrid()
        self.pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=10)
        self.sub = rospy.Subscriber('/map', OccupancyGrid, self.updateGrid, queue_size=10)
        self.angular_vel = angular_vel
        self.goalID = 0

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)
        self.occ_grid.tf_buffer = self.tf_buffer
        self.occ_grid.tf_buffer = self.tf_buffer

    
    def updateGrid(self, grid_msg):
        print("info")
        print(grid_msg.info)
        print("header")
        print(grid_msg.header)

        self.occ_grid.readOccupancyGrid(grid_msg)

    def rotate(self, length):
        twistMsg = Twist() 
        twistMsg.linear.x = 0
        twistMsg.linear.y = 0
        twistMsg.linear.z = 0
        twistMsg.angular.x = 0
        twistMsg.angular.y = 0
        twistMsg.angular.z = self.angular_vel    # set angular velocity

        end_t = rospy.Time.now() + rospy.Duration(length)

        print("start rotating")
        while not rospy.is_shutdown() and rospy.Time.now() < end_t: 
            self.pub.publish(twistMsg)
        # stop rotation
        twistMsg.angular.z = 0
        self.pub.publish(twistMsg)
        print("finish rotating")

        return True

    def curr_robo_coords(self, world_frame, robo_frame):
        """Return x, y, z of robo w.r.t world_frame"""
        trans = None
        try:
            trans = self.tf_buffer.lookup_transform(world_frame, robo_frame, rospy.Time())
            (trans, rot) = (trans.transform.translation, trans.transform.rotation)
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            print("Failed to get curr robo coords ")

        
        return trans 

    def move(self, goal, robot_frame, world_frame):
        """Move to goal, where goal is specified w.r.t the world frame"""

        # origin_x_world, origin_x_world = 
        robo_x_world, robo_y_world, _ = self.curr_robo_coords(world_frame, robot_frame)
        # get a bunch of waypoints using A* on the instantaneous occupancy grid


    def explore(self):
        done = False
        print("exploring")
        while not rospy.is_shutdown() and not done:
            self.rotate(ROTATE_TIME)
            robo_coords_odom = self.curr_robo_coords(WORLD_FRAME, ROBOT_FRAME) # odom frame is world frame
            while not robo_coords:
                print("Robo coords not neceived yet")
                rospy.sleep(1)
                robo_coords_odom = self.curr_robo_coords(WORLD_FRAME, ROBOT_FRAME) # odom frame is world frame

            while not self.occ_grid.mapLoaded():
                print("Map not neceived yet")
                rospy.sleep(1)

            goal = self.occ_grid.getClosestFrontierCentroidOdom(robo_coords_odom.x, robo_coords_odom.y)
            rospy.sleep(5)
            # self.move(goal, WORLD_FRAME)
            # done = self.occ_grid.num_frontier_pts < STOPPING_FRONTIER_PTS_NUM

    def occgrid_callback(self, grid):
        print(grid)

    def vacuum():
        pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=10)
        sub = rospy.Subscriber('/rtabmap/octomap_grid', OccupancyGrid, occgrid_callback, queue_size=10)
        # tfBuffer = tf2_ros.Buffer()
        # tfListener = tf2_ros.TransformListener(tfBuffer)
        # Create a timer object that will sleep long enough to result in
        # a 10Hz publishing rate
        r = rospy.Rate(10) # 10hz

        K1 = 0.3
        K2 = 1
        # Loop until the node is killed with Ctrl-C
        while not rospy.is_shutdown():
            try:
            #TODO: Replace 'SOURCE FRAME' and 'TARGET FRAME' with the appropriate TF frame names.
            # trans = tfBuffer.lookup_transform(robot_frame, target_frame, rospy.Time())
            # Process trans to get your state error
            # Generate a control command to send to the robot
                control_command = Twist() #TODO: Generate this
                control_command.linear.x = 0.2
                # control_command.linear.y = 0.1

                # control_command.angular.z = K2 * (trans.transform.translation.y)

                #################################### end your code ###############
                pub.publish(control_command)
            except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
                pass
            # Use our rate object to sleep until it is time to publish again
            r.sleep()



if __name__ == '__main__':
    # run orbslam2 node and occupancy grid generator so I can assume I have a map structure to perform
    # 
    import rospy
    rospy.init_node('turtlebot_controller', anonymous=True)
    tesroo = TesRoo()
    tesroo.explore()
    print("TesRoo has finised exploring, starting vacuuming")
    print("Would you like me to avoid any rooms? If so, please choose from the following options: None, Kitchen, Dining, Bed")
    tesroo.vacuum()
