# from Collections import deque
from geometry_msgs.msg import Twist
from nav_msgs.msg import OccupancyGrid
import tf2_ros
import sys

# def is_frontier_pt(map, pt):
#     """frontier point is an *unknown* (i.e. not a point formally in the map) 
#     point that has at least one open-space neighbor. Need to distinguish betweeen
#     a wall and an unknown point...
#     """
    
#     return 

# def explore_frontier(map, pose):
#     """Return next x, y position in the map to travel to
    
#     @Parameters
#     pose: 
#         global position of robot
#     map:
#         map
    
#     see link to Frontier Based Exploration for Autonomous Robot paper
#     """
#     # after unpacking or transforming map into 
#     map_open_lst = set()
#     map_close_lst = set()
#     frontier_open_lst = set() # pts enqueued by inner BFS
#     frontier_close_lst = set() # ptr dequeued by inner BFS

#     q_m = deque([])
#     q_f = deque([])

#     q_m.append(pose)
#     map_open_lst.add(pose)
#     while len(q_m) != 0:
#         p = q_m.pop_left()
#         if p in map_close_lst:
#             continue
#         if p in frontie

class Explorer:
    def __init__(self, angular_vel=0.2):
        self.occ_grid = OccupancyGrid()
        self.pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=10)
        self.sub = rospy.Subscriber('/rtabmap/octomap_grid', OccupancyGrid, queue_size=10)
        self.angular_vel = angular_vel

    def rotate(self):
        twistMsg = Twist() 
        twistMsg.linear.x = 0
        twistMsg.linear.y = 0
        twistMsg.linear.z = 0
        twistMsg.angular.x = 0
        twistMsg.angular.y = 0
        twistMsg.angular.z = self.angular_vel    # set angular velocity


        # time to stop rotation
        end_t = rospy.Time.now() + rospy.Duration(10)
        while not rospy.is_shutdown() and rospy.Time.now() < end_t: 
            self.pub.publish(twistMsg)
        
        # stop rotation
        twistMsg.angular.z = 0
        self.pub.publish(twistMsg)
        return True


    def explore(self):
        done = False
        while not rospy.is_shutdown() and not done:
            self.rotate()
            print("rotated once")
            self.occ_grid.getNearestFrontierCentroid()
            # poseStamp = geometry_msgs.msg.PoseStamped()
            # TODO populate poseStamp entries
            # pub.publish(poseStamp)


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
    explorer = Explorer()
    explorer.explore()
    print("Finised exploring, starting vacuuming")
