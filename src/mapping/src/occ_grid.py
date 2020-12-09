class OccupancyGrid:
    def __init__(self):
        self.isMapLoaded = False
        self.resolution = 0
        self.width = 0
        self.height = 0
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
        return

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

    def grid2world(self):
        return
