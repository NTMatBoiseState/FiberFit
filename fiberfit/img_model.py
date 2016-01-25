"""
Class representing a an imgage model, encapsulating th and k.
"""
class ImgModel:
    count = 0  # for all classes count starts from 0

    def __init__(self, filename,sig = None, k=None, th=None, R2=None, orgImg=None, orgImgEncoded=None, logScl=None,
                 logSclEncoded=None,  angDist=None, angDistEncoded=None, cartDist=None,
                 cartDistEncoded=None, timeStamp=None):
        self.filename = filename
        self.sig = sig,
        self.th = th
        self.k = k
        self.R2 = R2
        self.orgImg = orgImg
        self.orgImgEncoded = orgImgEncoded
        #self.orgImg4 = orgImg4
        #self.orgImgEncoded4 = orgImgEncoded4
        self.logScl = logScl
        self.logSclEncoded = logSclEncoded
        #self.logScl4 = logScl4
        #self.logSclEncoded4 = logSclEncoded4
        self.angDist = angDist
        self.angDistEncoded = angDistEncoded
        #self.angDist4 = angDist4
        #self.angDistEncoded4 = angDistEncoded4
        self.cartDist = cartDist
        self.cartDistEncoded = cartDistEncoded
        #self.cartDist4 = cartDist4
        #self.cartDistEncoded4 = cartDistEncoded4
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

