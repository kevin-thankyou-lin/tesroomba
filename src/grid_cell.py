class GridCell:
    def __init__(self, x=None, y=None, prob=-1, isOnFrontier=False, frontierClass=None):
        self.x = x
        self.y = y
        self.prob = prob
        self.isOnFrontier = isOnFrontier
        self.frontierClass = frontierClass
    
    def setXY(self, x, y):
        self.x = x
        self.y = y

    def setProb(self, prob):
        self.prob = prob

    def setIsOnFrontier(self, isOnFrontier):
        self.isOnFrontier = isOnFrontier

    def setFrontierClass(self, frontierClass):
        print("set frontier class to")
        print(frontierClass)
        self.frontierClass = frontierClass

    def getXY(self):
        return (self.x, self.y)

    def getIsOnFrontier(self):
        return self.isOnFrontier

    def getFrontierClass(self):
        return self.frontierClass

    def getProb(self):
        return self.prob

