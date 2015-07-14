"""
Class representing a an imgage model, encapsulating th and k.
"""
class ImgModel:
    count = 0 # for all classes count starts from 0
    def __init__(self, filename, k, th, figure, orgImg, logScl, angDist, cartDist, timeStamp, used=False ):
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


    #
    # def getTh(self):
    #    return self.th
    #
    # images[1].th
    #
    # -> later we want encapsulation, oh no!
    # => Properties to the rescue!
    #
    # class ImgModel:
    #     ...
    #     @property
    #     def getTh(self):
    #        return self.th / 180.0
    #
    # Now, call imageModel01.th becomes => imageModel01.getTh()


