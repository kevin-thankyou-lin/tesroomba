from grid_cell import GridCell
from collections import deque
import matplotlib.pyplot as plt 

class OccGrid:
    def __init__(self):
        self.occ_grid_2d = None
        self.occ_grid_2d_pure = None
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

    def getNearestFrontierCentroidWorld(self):
        grid_x, grid_y = self.getNearestFrontierCentroid()
        return self.grid2world(grid_y, grid_y)

    def getNearestFrontierCentroid(self):
        return

    def readOccupancyGrid(self, grid_msg):
        self.isMapLoaded = self.loadGridMetadata(grid_msg)
        assert self.isMapLoaded

        self.occ_grid_2d = []
        cell_idx = 0
        for h in range(self.height):
            width_arr = []
            for w in range(self.width):
                map_cell = GridCell(h, w)
                cell_idx = h * self.width + w
                map_cell.setProb(grid_msg.data[cell_idx])
                # if grid_msg.data[cell_idx] == 0:
                #     print("added a free cell")
                width_arr.append(map_cell)
                cell_idx += 1
            self.occ_grid_2d.append(width_arr)

        return True

    def isFrontier(self, cell):
        """
        Frontiers are regions on the boundary between unexplored and explored space

        Define frontier as a known free point that has at least one unknown neighbor
        """
        # print("isFrontier called")
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

    def classifyFrontiers(self):
        """
        Assigns class ID to all grid cells 
        @Return
        dict: {int: list[GridCell]} 
            dict mapping an ID to list of all grid cells with that ID
        """
        res = {0:[]}
        class_id = 0
        frontiers = self.frontiers_pts

        for f in frontiers:
            q = deque([])
            #  q invariant: everyone added must be a frontier with its class not assigned yet
            if f.getFrontierClass() != None:
                continue
            q.append(f)
            class_lst = res[class_id]
            # if curr pt doesn't have a class, 
            while q:
                curr_f = q.popleft()
                curr_f.setFrontierClass(class_id)
                class_lst.append(class_id)
                neighbors = self.getNeighbors(curr_f.getXY()[0], curr_f.getXY()[1])
                print(neighbors)
                for nei in neighbors:
                    if nei.getIsOnFrontier():
                        if nei.getFrontierClass != None:
                            q.append(nei)
            
            class_id += 1
            res[class_id] = []

        self.id_to_frontier_pts = res

    def getNeighbors(self, h, w):
        res = []
        for dh, dw in self.neighbor_idxs: # can optimize this 
            if 0 <= dh + h < self.height and 0 <= dw + w < self.width:
                nei = self.occ_grid_2d[dh + h][dw + w]
                res.append(nei) 
        return res

    def getFrontierCentroids(self):
        
        res = []
        for id, vals in self.id_to_frontier_pts:
            sum_x, sum_y = 0, 0
            for vx, vy in vals:
                sum_x += vx
                sum_y += vy
            res.append((sum_x / len(vals), sum_y / len(vals)))

        return res

    def getFrontierCentroidsWorld(self):
        grid_x, grid_y = self.getFrontierCentroids()
        return self.grid2world(grid_x, grid_y)

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

    def grid2world(self, grid_x, grid_y):
        """Return world frame coordinates for corresponding grid world coordinates"""
        origin_x, origin_x = self.origin.x, self.origin.y
        world_x = origin_x + grid_x * self.resolution # not sure how grid_x and grid_y are relative to origin?
        world_y = origin_y + grid_y * self.resolution # not sure how grid_x and grid_y are relative to origin?
        return (world_x, world_y)

    def getClosestFrontierCentroidWorld(self, src_x, src_y):
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
        centroid_candidates = self.getFrontierCentroidsWorld()
        return min(centroid_candidates, key=lambda c: self.l2_distance(x, (src_x, src_y)))