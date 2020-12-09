class OccupancyGrid:
    def __init__(self):
        self.isMapLoaded = False
        self.resolution = None
        self.width = None
        self.height = None
        self.origin = None
        self.occ_grid_2d = None
    
    def loadGridMetadata(self, grid_msg):
        self.resolution = grid_msg.resolution
        self.width = grid_msg.width
        self.height = grid_msg.height
        self.origin = grid_msg.origin
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
        return self.getNearestFrontierCentroidWorld(grid_y, grid_y)

    def getNearestFrontierCentroid(self):
        return

    def readOccupancyGrid(self, grid_msg):
        return

    def isFrontier(self, x, y):
        return

    def getFrontierPoints(self, x, y):
        return

    def classifyFrontiers(self):
        return

    def getFrontierCentroid(self):
        return

    def detectFrontiersCenterWorld(self):
        return

    def grid2world(self, grid_x, grid_y):
        """Return world frame coordinates for corresponding grid world coordinates"""
        origin_x, origin_x = self.origin.x, self.origin.y
        world_x = origin_x + grid_x * self.resolution # not sure how grid_x and grid_y are relative to origin?
        world_y = origin_y + grid_y * self.resolution # not sure how grid_x and grid_y are relative to origin?
        return (world_x, world_y)
