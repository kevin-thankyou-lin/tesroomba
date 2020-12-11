from collections import deque
import matplotlib.pyplot as plt 
import numpy as np
import tf2_ros
import rospy

from grid_cell import GridCell

MIN_FRONTIER_CLASS_SIZE = 8
MIN_FRONTIER_DISTANCE = 10

class OccGrid:
    def __init__(self):
        self.occ_grid_2d = None
        # self.occ_grid_graph = nx.Graph()
        # metadata
        self.isMapLoaded = False
        self.resolution = None
        self.width = None
        self.height = None
        self.origin = None # geometry_msgs/Point
        self.num_frontier_pts = 0
        self.frontiers_pts = None
        self.id_to_frontier_pts = None # dict mapping class id to list of frontier point cells

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
        return self.grid2Map(grid_x, grid_y)

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
        self.isMapLoaded = True
        return True

    def isFrontier(self, cell):
        """
        Frontiers are regions on the boundary between unexplored and explored space

        Define frontier as a known free point that has at least one unknown neighbor
        """
        h, w = cell.getHW()
        num_unknown_neighbors = 0
        if cell.getProb() == 0:
            neighbors = self.getNeighbors(h, w)
            for (dh, dw) in self.neighbor_idxs:
                new_h, new_w = h + dh, w + dw
                if 0 <= new_h < self.height and 0 <= new_w < self.width and self.occ_grid_2d[new_h][new_w].getProb() == -1:
                    num_unknown_neighbors += 1
                    print("cell")
                    print(new_h, new_w)
            print(num_unknown_neighbors)
            return num_unknown_neighbors > 0

    def labelFrontierPoints(self):
        """
        Labels if a grid cell is a frontier for all points in grid
        Returns the number of frontier points
        """
        print("labelFrontierPoints")
        print("labelFrontierPoints")
        print("labelFrontierPoints")

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
            stk = []

            if f.getFrontierClass() != None:
                continue

            frontier_h, frontier_w = f.getHW()
            
            # at least one neighbor is a frontier and has a class assigned
            curr_id = None
            for nei in self.getNeighbors(frontier_h, frontier_w):
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
                frontier_h, frontier_w = curr_f.getHW()
                neighbors = self.getNeighbors(frontier_h, frontier_w)

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
        Returns a list of [h][w] points in the occ_grid of frontier centroids 
        - coords are w.r.t the occupancy grid 'frame'
        """
        print("getFrontierCentroids")
        res = []
        for idx, cells in self.id_to_frontier_pts.items():
            print(len(cells))
            if len(cells) == 0:
                continue
            sum_h, sum_w = 0, 0
            for cell in cells:
                sum_h += cell.getH()
                sum_w += cell.getW()
            res.append((idx, (sum_h / len(cells), sum_w / len(cells))))
        print("END getFrontierCentroids")

        return res

    # def getFrontierCentroidsMap(self):
    #     """
    #     Returns list of centroids denoted in the map tf frame
    #     """
    #     print("getFrontierCentroidsMap")
    #     frontierCentroids = self.getFrontierCentroids()
    #     world_coords = map(self.grid2world, frontierCentroids)
    #     print("END getFrontierCentroidsMap")

    #     return world_coords

    def grid2Map(self, grid_coords):
        """Return map frame coordinates for corresponding grid (h, w) coordinates"""
        origin_x, origin_y = self.origin.position.x, self.origin.position.y

        h, w = grid_coords
        map_x = origin_x + w * self.resolution # not sure how grid_x and grid_y are relative to origin?
        map_y = origin_y + h * self.resolution # not sure how grid_x and grid_y are relative to origin?
        return (map_x, map_y)
    
    def map2Odom(self, map_coords):
        """
        Return the odom coords of map coords
        Both params are tuples of doubles
        """
        map_wrt_odom = self.tf_translate('map', 'odom')
        x_odom, y_odom = map_wrt_odom.x + map_coords[0], map_wrt_odom.y + map_coords[1]
        return x_odom, y_odom

    def tf_translate(self, frame1, frame2):
        """For tf frames frame1 and frame2, get frame1's origin w.r.t to frame2"""
        tf_buffer = tf2_ros.Buffer()
        tf_listener = tf2_ros.TransformListener(tf_buffer)

        r = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():
            try:
                trans = tf_buffer.lookup_transform(frame2, frame1, rospy.Time())
                (trans, rot) = (trans.transform.translation, trans.transform.rotation)
                break
            except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
                print("tf_translate failed ")
                r.sleep()

        return trans

    def map2Grid(self, map_coords):
        """Translate map_coords (h, w) to occ_grid coords"""
        map_x, map_y = map_coords
        dx, dy = map_x - self.origin.position.x , map_y - self.origin.position.y 
        w = int(dx / self.resolution)
        h = int(dy / self.resolution)
        return (h, w)

    def getClosestFrontier(self, src_x, src_y):
        """
        @Params
        src_x:
            x coord of robot w.r.t to a world frame e.g. odom
        src_y:
            y coord of robot w.r.t to a world frame e.g. odom
        @Returns
            x, y tuple that represents the coords for the closest frontier centroid ('by the bird's eye') to src_x and src_y
        """

        self.labelFrontierPoints()
        self.classifyFrontiers()

        odom_wrt_map = self.tf_translate('odom', 'map')
        map_wrt_odom = self.tf_translate('map', 'odom')

        centroid_candidates = self.getFrontierCentroids() 

        src_x_map, src_y_map = odom_wrt_map.x + src_x, odom_wrt_map.y + src_y 
        src_x_grid, src_y_grid = self.map2Grid((src_x_map, src_y_map))
        src_grid = (src_x_grid, src_y_grid)

        closest_frontier_grid = None
        min_dist = np.float("inf")
        for class_idx, frontier_pts_grid in self.id_to_frontier_pts.items():
            if len(frontier_pts_grid) > MIN_FRONTIER_CLASS_SIZE:
                for frontier_pt_grid in frontier_pts_grid:
                    frontier_pt_grid = frontier_pt_grid.getHW()
                    frontier_dist = self.l2_distance(src_grid, frontier_pt_grid)
                    if min_dist > frontier_dist > MIN_FRONTIER_DISTANCE:
                        closest_frontier_grid = frontier_pt_grid
                        min_dist = frontier_dist

        if not closest_frontier_grid:
            assert closest_frontier_grid

        print("closest_frontier_grid")
        print(closest_frontier_grid)
        closest_frontier_map = self.grid2Map(closest_frontier_grid)
        closest_frontier_x_odom, closest_frontier_y_odom = map_wrt_odom.x + closest_frontier_map[0], map_wrt_odom.y + closest_frontier_map[1]

        print(closest_frontier_x_odom, closest_frontier_y_odom)
        
        return (closest_frontier_x_odom, closest_frontier_y_odom)


    #####################
    # Utility Functions #
    #####################

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