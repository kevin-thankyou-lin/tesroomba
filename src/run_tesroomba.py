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

WORLD_FRAME = "odom"
STOPPING_FRONTIER_PTS_NUM = 5

class TesRoo:
    def __init__(self, angular_vel=0.2):
        self.occ_grid = OccGrid()
        self.pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=10)
        self.sub = rospy.Subscriber('/map', OccupancyGrid, self.occ_grid.readOccupancyGrid, queue_size=10)
        self.angular_vel = angular_vel
        self.goalID = 0
        self.tf_listener = tf.TransformListener()

        # # Create action client
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        rospy.loginfo("Waiting for move_base action server...")
        wait = self.move_base.wait_for_server(rospy.Duration(10.0))
        if not wait:
            rospy.logerr("Action server not available!")
            rospy.signal_shutdown("Action server not available!")
            return
        rospy.loginfo("Connected to move base server")
        rospy.loginfo("Starting goals achievements ...")

    def rotate(self):
        twistMsg = Twist() 
        twistMsg.linear.x = 0
        twistMsg.linear.y = 0
        twistMsg.linear.z = 0
        twistMsg.angular.x = 0
        twistMsg.angular.y = 0
        twistMsg.angular.z = self.angular_vel    # set angular velocity

        end_t = rospy.Time.now() + rospy.Duration(10)

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
        try:
            (trans, rot) = self.tf_listener.lookupTransform(world_frame, robo_frame, rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            print("Move failed :)")

        return trans 

    def move(self, goal, world_frame):
        """Move to goal, where goal is specified w.r.t the world frame"""

        robo_x, robo_y, _ = self.curr_robo_coords("odom", "base_link")
        # get a bunch of waypoints using A* on the instantaneous occupancy grid


    def explore(self):
        done = False
        while not rospy.is_shutdown() and not done:
            self.rotate()
            goal = (goal_x, goal_y) = self.occ_grid.getClosestFrontierCentroidWorld()
            self.move(goal)
            done = self.occ_grid.num_frontier_pts < STOPPING_FRONTIER_PTS_NUM

    def occgrid_callback(self, grid):
        import ipdb;ipdb.set_trace()
        print(grid)

    def vacuum():
        pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=10)
        sub = rospy.Subscriber('/rtabmap/octomap_grid', OccupancyGrid, occgrid_callback, queue_size=10)
        tfBuffer = tf2_ros.Buffer()
        tfListener = tf2_ros.TransformListener(tfBuffer)
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
