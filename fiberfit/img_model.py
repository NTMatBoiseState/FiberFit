"""
Class representing a an imgage model, encapsulating th and k.
"""
class imgModel:
    count = 0 # for all classes count starts from 0
    def __init__(self, th = None, k = None, figure = None):
        self.th = th
        self.k = k
        self.figure = figure
    def __repr__(self):
        return "image" + str(self.count)
    def getTh(self):
        return self.th
    def getK(self):
        return self.k