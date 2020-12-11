from collections import deque
import matplotlib.pyplot as plt 
import numpy as np
import tf2_ros
import rospy

from grid_cell import GridCell


class OccGrid:
    def __init__(self):
        self.occ_grid_2d = None
        # metadata
        self.isMapLoaded = False
        self.resolution = None
        self.width = None
        self.height = None
        self.origin = None
        self.num_frontier_pts = 0
        self.frontiers_pts = None
        self.id_to_frontier_pts = None

        self.neighbor_idxs = [(x, y) for x in [-1, 0, 1] for y in [-1, 0, -1]]
        self.neighbor_idxs.remove((0, 0))

    def mapLoaded(self):
        return self.isMapLoaded

    def loadGridMetadata(self, grid_msg):
        self.resolution = grid_msg.info.resolution
        self.width = grid_msg.info.width
        self.height = grid_msg.info.height
        self.origin = grid_msg.info.origin
        return True
        
    def getResolution(self):
        assert self.isMapLoaded
        return self.resolution

    def getWidth(self):
        assert self.isMapLoaded
        return self.width

    def getHeight(self):
        assert self.isMapLoaded
        return self.height

    def getOrigin(self):
        assert self.isMapLoaded
        return self.origin

    def getNearestFrontierCentroidMap(self):
        grid_x, grid_y = self.getNearestFrontierCentroid()
        return self.grid2Map(grid_y, grid_y)

    def getNearestFrontierCentroid(self):
        return

    def readOccupancyGrid(self, grid_msg):
        """Read in the new grid data: update 2d grid and metadata"""
        self.loadGridMetadata(grid_msg)

        res = []
        cell_idx = 0
        for h in range(self.height):
            width_arr = []
            for w in range(self.width):
                map_cell = GridCell(h, w)
                map_cell.setProb(grid_msg.data[cell_idx])
                width_arr.append(map_cell)
                cell_idx += 1
            res.append(width_arr)

        self.occ_grid_2d = res
        print("post reading occ grid")
        print(self.height, self.width)
        print(len(self.occ_grid_2d), len(self.occ_grid_2d[0])) 
        print("heights vs reality")
        self.isMapLoaded = True
        return True

    def isFrontier(self, cell):
        """
        Frontiers are regions on the boundary between unexplored and explored space

        Define frontier as a known free point that has at least one unknown neighbor
        """
        x, y = cell.getXY()
        num_unknown_neighbors = 0
        if cell.getProb() == 0:
            for h, w in self.neighbor_idxs:
                    new_h = x + h
                    new_w = y + w
                    if 0 <= new_h < self.height and 0 <= new_w < self.width and self.occ_grid_2d[new_h][new_w].getProb() == -1:
                        num_unknown_neighbors += 1
            return num_unknown_neighbors > 0

    def labelFrontierPoints(self):
        """
        Labels if a grid cell is a frontier for all points in grid
        Returns the number of frontier points
        """
        frontiers = []
        for h in range(self.height):
            for w in range(self.width):
                cell = self.occ_grid_2d[h][w]
                if cell.getProb() == 0:
                    if self.isFrontier(cell):
                        cell.setIsOnFrontier(True)
                        frontiers.append(cell)

        self.num_frontier_pts = len(frontiers)
        self.frontiers_pts = frontiers
        print("finish labelling frontier points")

    def classifyFrontiers(self):
        """
        Assigns class ID to all grid cells 
        @Return
        dict: {int: list[GridCell]} 
            dict mapping an ID to list of all grid cells with that ID

        loop through all frontier points f

        check if f already has a class
        if so, skip updating f's class id
        if no, we must assign an ID to f
            check if f has any frontier neighbors:
                if no, use the newest class id available and increment class 
                if so, get first neighbor's class and exist this f

        """
        print("classifyFrontiers")

        new_class_id = 0
        id_to_pts = {new_class_id : []}

        frontiers = self.frontiers_pts
        # dumb method for class assignment ...
        for f in frontiers:
            f.setFrontierClass(None)

        for f in frontiers:
            print("f")
            print(f.getXY())
            stk = []

            if f.getFrontierClass() != None:
                continue

            frontier_x, frontier_y = f.getXY()
            
            # at least one neighbor is a frontier and has a class assigned
            curr_id = None
            for nei in self.getNeighbors(frontier_x, frontier_y):
                if nei.getIsOnFrontier() and nei.getFrontierClass() != None:
                    curr_id = nei.getFrontierClass()
                    f.setFrontierClass(curr_id)
                    if curr_id not in id_to_pts:
                        id_to_pts[curr_id] = []
                    id_to_pts[curr_id].append(f)
                    break

            if curr_id == None:
                curr_id = new_class_id
                new_class_id += 1
                
            stk.append(f)

            while stk and not rospy.is_shutdown():
                # convert everyone that's connect to f to curr_id if they don't have a class already
                curr_f = stk.pop()
                curr_f.setFrontierClass(curr_id)

                if curr_id not in id_to_pts:
                    id_to_pts[curr_id] = []
                
                id_to_pts[curr_id].append(curr_f)
                frontier_x, frontier_y = curr_f.getXY()
                neighbors = self.getNeighbors(frontier_x, frontier_y)

                for nei in neighbors:
                    if nei.getIsOnFrontier():
                        if nei.getFrontierClass() != curr_id:
                            stk.append(nei)
                            curr_f.setFrontierClass(curr_id)
            
        self.id_to_frontier_pts = id_to_pts
        print("END: classifyFrontiers")


    def getNeighbors(self, h, w):
        res = []
        for dh, dw in self.neighbor_idxs: # can optimize this 
            if 0 <= dh + h < self.height and 0 <= dw + w < self.width:
                nei = self.occ_grid_2d[dh + h][dw + w]
                res.append(nei) 
        return res

    def getFrontierCentroids(self):
        """
        Returns a list of (x, y) points in the occ_grid of frontier centroids 
        - coords are w.r.t the occupancy grid 'frame'
        """
        print("getFrontierCentroids")
        res = []
        for idx, cells in self.id_to_frontier_pts.items():
            print(len(cells))
            if len(cells) == 0:
                continue
            sum_x, sum_y = 0, 0
            for cell in cells:
                sum_x += cell.getX()
                sum_y += cell.getY()
            res.append((sum_x / len(cells), sum_y / len(cells)))
        print("END getFrontierCentroids")

        return res

    def getFrontierCentroidsMap(self):
        """
        Returns list of centroids denoted in the map tf frame
        """
        print("getFrontierCentroidsMap")
        frontierCentroids = self.getFrontierCentroids()
        world_coords = map(self.grid2world, frontierCentroids)
        print("END getFrontierCentroidsMap")

        return world_coords

    def l2_distance(self, source, target):
        """Compute straight line distance between source point and target point.
        Source and target are both in world coordinates
        
        @Params
        source: tuple (int, int)
        target: tuple (int, int)

        @Returns
        double
        """
        return np.sqrt((source[0] - target[0])**2 + (source[1] - target[1])**2)

    def grid2Map(self, grid_coords):
        """Return map frame coordinates for corresponding grid coordinates"""
        origin_x, origin_y = self.origin.position.x, self.origin.position.y
        map_x = origin_x + grid_coords[0] * self.resolution # not sure how grid_x and grid_y are relative to origin?
        map_y = origin_y + grid_coords[1] * self.resolution # not sure how grid_x and grid_y are relative to origin?
        while not rospy.is_shutdown():
            try:
                trans = self.tf_buffer.lookup_transform("odom", "map", rospy.Time())
                (trans, rot) = (trans.transform.translation, trans.transform.rotation)
                continue
            except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
                print("Failed to get curr robo coords ")

        odom_x = map_x + trans.x
        odom_y = map_y + trans.y
        return (odom_x, odom_y)
    
    def tf_translate(self, frame1, frame2):
        """For tf frames frame1 and frame2, get frame1's origin w.r.t to frame2"""
        tf_buffer = tf2_ros.Buffer()
        tf_listener = tf2_ros.TransformListener(tf_buffer)
        while not rospy.is_shutdown():
            try:
                trans = tf_buffer.lookup_transform("frame2", "frame1", rospy.Time())
                (trans, rot) = (trans.transform.translation, trans.transform.rotation)
                continue
            except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
                print("Failed to get curr robo coords ")

        return trans

    def map2Grid(self, map_coords):
        """Translate map_coords (x, y) to occ_grid coords"""
        map_x, map_y = map_coords
        dx, dy = self.origin.x - map_x, self.origin.y - map_y
        w = int(dx / self.resolution)
        h = int(dy / self.resolution)
        return (h, w)

    def getClosestFrontierCentroidOdom(self, src_x, src_y):
        """
        @Params
        src_x:
            x coord of robot w.r.t to a world frame e.g. odom
        src_y:
            y coord of robot w.r.t to a world frame e.g. odom
        @Returns
            x, y tuple that represents the coords for the closest frontier centroid ('by the bird's eye') to src_x and src_y
        """
        if not self.isMapLoaded:
            print("Map hasn't been loaded yet :(, please wait")
            return False

        self.labelFrontierPoints()
        self.classifyFrontiers()

        centroid_candidates = self.getFrontierCentroidsWorld()
        print("closest frontier centroid is ")
        print(src_x, src_y)
        print(min(centroid_candidates, key=lambda c: self.l2_distance(c, (src_x, src_y))))
        
        return min(centroid_candidates, key=lambda c: self.l2_distance(c, (src_x, src_y)))