"""
Class representing a an imgage model, encapsulating th and k.
"""
class imgModel:
    count = 0 # for all classes count starts from 0
    def __init__(self, filename = None, th = None, k = None, figure = None, used = None):
        self.filename = filename
        self.th = th
        self.k = k
        self.figure = figure
        self.used = used

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