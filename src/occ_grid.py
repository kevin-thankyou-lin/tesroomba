from grid_cell import GridCell

class OccGrid:
    def __init__(self):
        self.isMapLoaded = False
        self.resolution = None
        self.width = None
        self.height = None
        self.origin = None
        self.id_to_frontier_pts = dict()
        self.occ_grid_2d = []
    
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
                width_arr.append(map_cell)
                cell_idx += 1

        return True

    def isFrontier(self, x, y):
        """
        Frontiers are regions on the boundary between unexplored and explored space

        Define frontier as a known free point that has at least one unknown neighbor
        """
        num_unknown_neighbors = 0
        if self.occ_grid_2d[x][y].getProb() == 0:
            for h in range(-1, 2):
                for w in range(-1, 2):
                    new_h = x + h
                    new_w = y + w
                    if 0 <= new_h < self.height and 0 <= new_w < self.height and 10 >= self.occ_grid_2d[new_h][new_w].getProb() == -1:
                        num_unknown_neighbors += 1
            return num_unknown_neighbors > 0
        else:
            return False

    def getFrontierPoints(self):
        """
        Sets if a grid cell is a frontier for all points in grid
        Returns the number of frontier points
        """
        num_frontiers = 0
        for h in range(self.height):
            for w in range(self.width):
                if self.occ_grid[h][w].getProb() == -1:
                    isOnFrontier = self.isFrontier(h, w)
                    occupancyMap[h][w].setIsOnFrontier(isOnFrontier)
      
        if isOnFrontier:
            num_frontiers += 1
      
        return num_frontiers

    def classifyFrontiers(self):
        """
        Goes through all grid cells and gives cells a frontier class ID
        """
        class_id = 0
        for h in range(self.height):
            for w in range(self.width):
                if self.occ_grid[h][w].getProb() == -1:
                    isOnFrontier = self.isFrontier(h, w)
                    occupancyMap[h][w].setIsOnFrontier(isOnFrontier)
        return

    def getFrontierCentroids(self):
        x, y = 0, 0


        return x, y

    def getFrontierCentroidsWorld(self):
        grid_x, grid_y = self.getFrontierCentroid()
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

    def getClosestFrontierCentroid(self, src_x, src_y):
        """
        @Params
        src_x:
            x coord of robot w.r.t to a world frame e.g. odom
        src_y:
            y coord of robot w.r.t to a world frame e.g. odom
        @Returns
            x, y tuple that represents the coords for the closest frontier centroid ('by the bird's eye') to src_x and src_y
        """
        centroid_candidates = self.getFrontierCentroidsWorld()
        return min(centroid_candidates, key=lambda c: self.l2_distance(x, (src_x, src_y)))