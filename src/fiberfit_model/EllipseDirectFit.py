from __future__ import division
# try:
#     from runtime import *
# except ImportError:
#     from smop.runtime import *

from src.fiberfit_model.helpers import debug
import numpy as np
from numpy.linalg import eig, inv
import scipy.ndimage
from pylab import *


def EllipseDirectFit(XY):
    centroid = np.mean(XY, axis=0)
    e1 = (XY[:, 0] - centroid[0]) ** 2
    e2 = (XY[:, 0] - centroid[0]) * ((XY[:, 1] - centroid[1]))
    e3 = (XY[:, 1] - centroid[1]) ** 2
    D1 = np.vstack(([e1, e2, e3])).T
    f1 = XY[:, 0] - centroid[0]
    f2 = XY[:, 1] - centroid[1]
    f3 = np.ones((1, XY.shape[0]))
    D2 = vstack(([f1, f2, f3])).T
    S1 = dot(D1.T, D1)
    S2 = dot(D1.T, D2)
    S3 = dot(D2.T, D2)
    T = dot(-linalg.inv(S3), S2.T)
    M = S1 + (dot(S2, T))
    M = np.vstack(([M[2, :] / 2, - M[1, :], M[0, :] / 2]))
    _eval, evec = linalg.eig(M)
    cond = (4 * evec[0, :] * evec[2, :]) - (evec[1, :] ** 2)
    A1 = evec[:, nonzero(cond > 0)[0]]
    A = np.vstack((A1, dot(T, A1)))
    A3 = A[3] - 2 * A[0] * centroid[0] - A[1] * centroid[1]
    A4 = A[4] - 2 * A[2] * centroid[1] - A[1] * centroid[0]
    A5 = A[5] + A[0] * centroid[0] ** 2 + A[2] * centroid[1] ** 2 + A[1] * centroid[0] * centroid[1] - A[3] * centroid[
        0] - A[4] * centroid[1]
    A[3] = A3
    A[4] = A4
    A[5] = A5
    A = A / linalg.norm(A)
    return A, centroid

