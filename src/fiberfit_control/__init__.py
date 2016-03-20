import matplotlib

matplotlib.use("Qt5Agg")  ## forces to use Qt5Agg so that Backends workfrom fiberfit import fiberfit_GUI
# matplotlib.use('Agg')
import numpy as np
import scipy
import scipy.ndimage
import scipy.interpolate
import scipy.optimize
import scipy.integrate
import math
import glob
from pylab import *
from pandas import DataFrame
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import argparse, re, os, glob, sys, pprint, itertools
import inspect


# from matplotlib.patches import Ellipse

# from __future__ import division
# try:
#     from runtime import *
# except ImportError:
#     from smop.runtime import *

from fiberfit.EllipseDirectFit import *  # XXX: Changed here
from fiberfit.helpers import *
from helpers import debug

import sys
import matplotlib

matplotlib.use("Qt5Agg")  ## forces to use Qt5Agg so that Backends workfrom fiberfit import fiberfit_GUI
from fiberfit import computerVision_BP
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.Qt import *
from PyQt5 import QtCore

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

from PyQt5 import QtCore, QtGui, QtWidgets
