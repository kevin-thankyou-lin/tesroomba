from collections import deque

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
import networkx as nx 

from math import atan2, sin, cos, pow, sqrt


WORLD_FRAME = "odom" # world frame is the odom frame - map from moves w.r.t to the move frame!
ROBOT_FRAME = "base_link"

STOPPING_FRONTIER_PTS_NUM = 20
ROTATE_TIME = 5
MAX_DIST_PER_WAYPOINT = 0.5 # this is in meters
ROTATION_VELOCITY = 0.5

class TesRoo:
    def __init__(self, angular_vel=ROTATION_VELOCITY):
        self.occ_grid = OccGrid()
        self.free_graph = nx.Graph()
        self.pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=10)
        self.sub = rospy.Subscriber('/map', OccupancyGrid, self.updateDataStructures, queue_size=10)
        
        self.angular_vel = angular_vel
        self.goalID = 0

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)
        self.occ_grid.tf_buffer = self.tf_buffer
        self.occ_grid.tf_buffer = self.tf_buffer

    def updateDataStructures(self, grid_msg):
        print("info")
        # print(grid_msg.info)
        print("header")
        # print(grid_msg.header)

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
        rate = rospy.Rate(10)
        while not rospy.is_shutdown() and rospy.Time.now() < end_t: 
            self.pub.publish(twistMsg)
            rate.sleep()

        twistMsg.angular.z = 0
        self.pub.publish(twistMsg)
        print("finish rotating")

        return True

    def curr_robo_pose(self, world_frame, robo_frame):
        """Return x, y, z of robo w.r.t world_frame"""
        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            try:
                trans = self.tf_buffer.lookup_transform(world_frame, robo_frame, rospy.Time())
                return (trans.transform.translation, trans.transform.rotation)
            except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
                print("Failed to get curr robo coords ")
                r.sleep()


    def goToGoal(self, goal, world_frame, robot_frame):
        """Move to goal, where goal is specified w.r.t the world frame
        @Params
        goal : tuple (int, int)
        world_frame: use WORLD_FRAME global variable
        robot_frame: use ROBOT_FRAME global variable
        This goal is a longer goal so we create a list of waypoints for tesroo to hit"""

        # robo_coords_odom, _ = self.curr_robo_pose(world_frame, robot_frame)
        # get a bunch of waypoints using A* on the instantaneous occupancy grid
        # @Neha                             @Neha                          @Neha                        @Neha
        self.moveTo(goal, world_frame, robot_frame)
        # waypoints = self.get_waypoints()
        # for wp in waypoints:
        #     self.moveTo(wp, world_frame, robo_frame)

    def moveTo(self, target, world_frame, robot_frame):
        """Take Tesroo from its current position to target take a straight line 
        First, we rotate to orient ourselves in the correct direction. 
        Then, we drive straight until we're there

        @Params
        target: tuple
        """    
        r = rospy.Rate(4)
        move_forward = False 

        while not rospy.is_shutdown():
            robo_coords_odom, robo_rot = self.curr_robo_pose(world_frame, robot_frame)
            target_x, target_y = target
            curr_x, curr_y = robo_coords_odom.x, robo_coords_odom.y

            (roll, pitch, theta) = tf.transformations.euler_from_quaternion([robo_rot.x, robo_rot.y, robo_rot.z, robo_rot.w])
            
            inc_x = target_x - curr_x 
            inc_y = target_y - curr_y 

            angle_to_goal = atan2(inc_y, inc_x) 
            dist = sqrt(pow(inc_x, 2) + pow(inc_y, 2))      #calculate distance
            turn = atan2(sin(angle_to_goal - theta), cos(angle_to_goal - theta))

            if dist < 0.1:
                return
            
            if abs(angle_to_goal - theta) < 0.1:    #0.1 because it too exact for a robot if both angles should be exactly 0
                move_forward = True

            control_command = Twist() 
            control_command.angular.z = 0.2 * turn

            if move_forward == True:
                #keep speed between 0.3 and 0.7
                if 0.1 * dist > 0.3 and 0.1 * dist < 0.7:
                    control_command.linear.x = 0.05 * dist
                elif 0.1 * dist > 0.7:
                    control_command.linear.x = 0.7
                else:
                    control_command.linear.x = 0.3

            self.pub.publish(control_command)
            r.sleep()


    def explore(self):
        done = False
        print("exploring")
        r1 = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown() and not done:
            self.rotate(ROTATE_TIME)
            robo_coords_odom, _ = self.curr_robo_pose(WORLD_FRAME, ROBOT_FRAME) # odom frame is world frame
            r2 = rospy.Rate(10) # 10hz
            while not self.occ_grid.mapLoaded():
                print("Map not neceived yet")
                r2.sleep()

            goal = self.occ_grid.getClosestFrontier(robo_coords_odom.x, robo_coords_odom.y)
            r1.sleep()

            self.goToGoal(goal, WORLD_FRAME, ROBOT_FRAME)
            done = self.occ_grid.num_frontier_pts < STOPPING_FRONTIER_PTS_NUM

    def occgrid_callback(self, grid):
        print(grid)

    def vacuum(self):
        print("start vacuuming")
        self.rotate(ROTATE_TIME)
        r2 = rospy.Rate(10) # 10hz
        while not self.occ_grid.mapLoaded():
            print("Map not neceived yet")
            r2.sleep()
        
        robo_coords_odom, robo_rot = self.curr_robo_pose(WORLD_FRAME, ROBOT_FRAME)

        free_cells = []
        occ_grid_2d = self.occ_grid.occ_grid_2d

        for h in range(self.occ_grid.getHeight()):
            for w in range(self.occ_grid.getWidth()):
                if occ_grid_2d[h][w].getProb() == 0:
                    free_cells.append(occ_grid_2d[h][w])
        
        for free_cell in free_cells:
            stk = [free_cell]
            while stk:
                curr_cell = stk.pop()
                curr_cell.setVacummed()
                goal_x_map, goal_y_map = self.occ_grid.grid2Map((curr_cell.getH(), curr_cell.getW()))
                goal_x_odom, goal_y_odom = self.occ_grid.map2Odom((goal_x_map, goal_y_map))
                self.goToGoal((goal_x_odom, goal_y_odom), WORLD_FRAME, ROBOT_FRAME)
                print("goals", (goal_x_odom, goal_y_odom))
                neighbors = self.occ_grid.getNeighbors(curr_cell.getH(), curr_cell.getW())
                for nei in neighbors:
                    if not nei.getVacummed():
                        stk.append(nei)
        


if __name__ == '__main__':
    # run orbslam2 node and occupancy grid generator so I can assume I have a map structure to perform
    # 
    import rospy
    rospy.init_node('turtlebot_controller', anonymous=True)
    tesroo = TesRoo()
    # tesroo.explore()
    print("TesRoo has finised exploring, starting vacuuming")
    print("Would you like me to avoid any rooms? If so, please choose from the following options: None, Kitchen, Dining, Bed")
    tesroo.vacuum()
    print("hi")
