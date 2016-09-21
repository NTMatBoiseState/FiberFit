import sys
sys.path.append("/fiberfit/")

class ImgModel:
    """
    Class representing an image model, encapsulating th and k.
    """
    count = 0  # for all classes count starts from 0

    def __init__(self, filename,sig = None, k=None, th=None, R2=None, orgImg=None, orgImgEncoded=None, logScl=None,
                 logSclEncoded=None,  angDist=None, angDistEncoded=None, cartDist=None,
                 cartDistEncoded=None, timeStamp=None, number = None):
        self.filename = filename
        self.sig = sig,
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
        self.number = number

    def _key(self):
        return self.filename

    def __eq__(self, other):
        return self._key() == other._key()

    def __hash__(self):
        return hash(self._key())

