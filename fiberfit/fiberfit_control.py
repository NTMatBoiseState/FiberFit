#!/usr/local/bin/python3

"""This is a control part of the GUI application"""

import sys
import matplotlib
matplotlib.use("Qt5Agg") ## forces to use Qt5Agg so that Backends work
from fiberfit import fiberfit_GUI
from fiberfit import computerVision_BP
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.Qt import*
from PyQt5 import QtCore

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure


class fft_mainWindow(fiberfit_GUI.Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self, Parent = None):
        super(fft_mainWindow, self).__init__()
        self.setupUi(self)
        self.startButton.clicked.connect(self.start)





    def start(self):
        computerVision_BP.fiberfit_model.main(self)
        image = QPixmap("image0");
        #image.scaledToHeight(10) NOT USEFUL
        #image.scaledToWidth(10) NOT USEFUL

        imageLabel = QtWidgets.QLabel()
        imageLabel.setPixmap(image)
        imageLabel.setScaledContents(True) # pretty much

        self.gridLayout.addWidget(imageLabel)
        #img = Figure()
        #fig = FigureCanvas.__init__(self, self.img)
        #self.gridLayout.addItem(fig)



        #fiberfit_GUI.Ui_MainWindow(self).gridLayout.addWidget(matplot widget goes here)

        #matplot = fiberfit_GUI.Ui_MainWindow

        #imgdata = io.BytesIO()
        #fig = Figure((5.0,4.0), dpi = 100)
        #canvas = FigureCanvas(fig)
        #self.gridLayout.addWidget(plt)
        #self.gridLayout.addWidget(computerVision_BP.fiberfit.fig)

       # canvas.setParent(matplot.frame)










app = QtWidgets.QApplication(sys.argv)
fft_app = fft_mainWindow()
fft_app.show()
sys.exit(app.exec_())


