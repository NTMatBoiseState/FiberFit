"""
Class representing a an imgage model, encapsulating th and k.
"""
class ImgModel:
    count = 0 # for all classes count starts from 0
    def __init__(self, filename, k= None, th = None, R2 = None, orgImg = None, orgImgEncoded = None, logScl = None, logSclEncoded = None, angDist = None, angDistEncoded = None, cartDist = None, cartDistEncoded = None, timeStamp = None):
        self.filename = filename
        self.th = th
        self.k = k
        self.R2 = R2
        self.orgImg = orgImg
        self.orgImgEncoded = orgImgEncoded
        self.logScl = logScl
        self.logSclEncoded = logSclEncoded
        self.angDist = angDist
        self.angDistEncoded = angDistEncoded
        self.cartDist = cartDist
        self.cartDistEncoded = cartDistEncoded
        self.timeStamp = timeStamp

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

