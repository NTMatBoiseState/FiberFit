"""
Class representing a an imgage model, encapsulating th and k.
"""
class imgModel:
    count = 0 # for all classes count starts from 0
    def __init__(self, filename = None, k = None, th = None, figure = None, orgImg = None, logScl = None, angDist = None, cartDist = None, used = None, timeStamp = None):
        self.filename = filename
        self.th = th
        self.k = k
        self.figure = figure
        self.orgImg = orgImg
        self.logScl = logScl
        self.angDist = angDist
        self.cartDist = cartDist
        self.used = used
        self.timeStamp = timeStamp

    def __repr__(self):
        return "image" + str(self.count)

    def getTh(self):
        return self.th

    def getK(self):
        return self.k

    def getFig(self):
        return self.figure

    def getName(self):
        return self.filename

    def setUsed(self, used):
        self.used = used

    def getUsed(self):
        return self.used

    def getTimeStamp(self):
        return self.timeStamp

    def getOriginalImg(self):
        return self.orgImg

    def getLogScl(self):
        return self.logScl

    def getAngDist(self):
        return self.angDist

    def getCartDist(self):
        return self.cartDist