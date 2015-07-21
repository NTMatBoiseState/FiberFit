"""
Class representing a an imgage model, encapsulating th and k.
"""
<<<<<<< HEAD


class ImgModel:
    count = 0  # for all classes count starts from 0

    def __init__(self, filename=None, k=None, th=None, orgImg=None, logScl=None, angDist=None,
                 cartDist=None, used=None, timeStamp=None):
=======
class ImgModel:
    count = 0 # for all classes count starts from 0
    def __init__(self, filename, k= None, th = None, orgImg = None, logScl = None, angDist = None, cartDist = None, timeStamp = None):
>>>>>>> CodeReview
        self.filename = filename
        self.th = th
        self.k = k
        self.orgImg = orgImg
        self.logScl = logScl
        self.angDist = angDist
        self.cartDist = cartDist
        self.timeStamp = timeStamp

<<<<<<< HEAD
    def getTh(self):
        return self.th

    def getK(self):
        return self.k

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
=======
    def _key(self):
        return (self.filename)

    def __eq__(self, other):
        return self._key() == other._key()

    def __hash__(self):
        return hash(self._key())

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


>>>>>>> CodeReview
