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

# def explore():
#     done = False
#     # TODO @Risham
#     sub = rospy.Subscriber('/occupancy_grid', occupancy_grid_type, queue_size=10)
#     pub = rospy.Publisher('/move_base/goal', geometry_msgs.msg.PoseStamped, queue_size=10)
#     while not done:
#         poseStamp = geometry_msgs.msg.PoseStamped()
#         # TODO populate poseStamp entries
#         pub.publish(poseStamp)


def occgrid_callback(grid):
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
        #print(trans)
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
    print("Finised exploring, starting vacuuming")
    vacuum()