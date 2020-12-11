class GridCell:
    def __init__(self, h=None, w=None, prob=-1, isOnFrontier=False, frontierClass=None):
        self.h = h
        self.w = w
        self.prob = prob
        self.isOnFrontier = isOnFrontier
        self.frontierClass = frontierClass
    
    def setHW(self, h, w):
        self.h = h
        self.w = w

    def setProb(self, prob):
        self.prob = prob

    def setIsOnFrontier(self, isOnFrontier):
        self.isOnFrontier = isOnFrontier

    def setFrontierClass(self, frontierClass):
        self.frontierClass = frontierClass

    def getHW(self):
        return (self.h, self.w)
    
    def getH(self):
        return self.h

    def getW(self):
        return self.w

    def getIsOnFrontier(self):
        return self.isOnFrontier

    def getFrontierClass(self):
        return self.frontierClass

    def getProb(self):
        return self.prob

