from Collections import deque

def is_frontier_pt(map, pt):
    """frontier point is an *unknown* (i.e. not a point formally in the map) 
    point that has at least one open-space neighbor. Need to distinguish betweeen
    a wall and an unknown point...
    """
    
    return 

def explore_frontier(map, pose):
    """Return next x, y position in the map to travel to
    
    @Parameters
    pose: 
        global position of robot
    map:
        map
    
    see link to Frontier Based Exploration for Autonomous Robot paper
    """
    # after unpacking or transforming map into 
    map_open_lst = set()
    map_close_lst = set()
    frontier_open_lst = set() # pts enqueued by inner BFS
    frontier_close_lst = set() # ptr dequeued by inner BFS

    q_m = deque([])
    q_f = deque([])

    q_m.append(pose)
    map_open_lst.add(pose)
    while len(q_m) != 0:
        p = q_m.pop_left()
        if p in map_close_lst:
            continue
        if p in frontie

def explore():
    done = False
    # TODO @Risham
    sub = rospy.Subscriber('/occupancy_grid', occupancy_grid_type, queue_size=10)
    pub = rospy.Subscriber('/move_base/goal', geometry_msgs.msg.PoseStamped, queue_size=10)
    while not done:
        poseStamp = geometry_msgs.msg.PoseStamped()
        # TODO populate poseStamp entries
        pub.publish(poseStamp)

def vacuum():
    pass


if __name__ == '__main__':
    # run orbslam2 node and occupancy grid generator so I can assume I have a map structure to perform
    # 
    explore()
    print("Finised exploring, starting vacuuming")
    vacuum()