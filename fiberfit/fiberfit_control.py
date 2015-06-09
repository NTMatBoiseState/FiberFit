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
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtCore

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure


class fft_mainWindow(fiberfit_GUI.Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self, Parent = None):
        super(fft_mainWindow, self).__init__()
        self.setupUi(self)
        self.indicator = 0
        self.isStarted = False
        self.startButton.clicked.connect(self.start)
        self.nextButton.clicked.connect(self.nextImage)
        self.prevButton.clicked.connect(self.prevImage)
        self.loadButton.clicked.connect(self.launch)

    def launch(self):
        dialog = QFileDialog()
        dialog.setWindowTitle("Select image")
        dialog.setNameFilter("Images (*.png)")
        dialog.setFileMode(QFileDialog.ExistingFile)
        #if dialog.exec_() == QtWidgets.QDialog.Accepted:
        #    self.filename = dialog.selectedFiles()[0]
        self.filename = dialog.getOpenFileNames()

    def processImages(self):
        self.image = QPixmap("image0");
        self.image1 = QPixmap("image1");
        self.image2 = QPixmap("image2");
        self.image3 = QPixmap("image3");

        self.imageLabel = QtWidgets.QLabel()
        self.imageLabel.setPixmap(self.image)

        self.imageLabel1 = QtWidgets.QLabel()
        self.imageLabel1.setPixmap(self.image1)

        self.imageLabel2 = QtWidgets.QLabel()
        self.imageLabel2.setPixmap(self.image2)

        self.imageLabel3 = QtWidgets.QLabel()
        self.imageLabel3.setPixmap(self.image3)

        self.imageLabel.setScaledContents(True)
        self.imageLabel1.setScaledContents(True)
        self.imageLabel2.setScaledContents(True)
        self.imageLabel3.setScaledContents(True)

    def start(self): #fix the restart option
        if (self.isStarted):
            if (self.indicator == 0):
                self.gridLayout.removeWidget(self.imageLabel)
            elif self.indicator == 1:
                self.gridLayout.removeWidget(self.imageLabel1)
            elif self.indicator == 2:
                self.gridLayout.removeWidget(self.imageLabel2)
            elif self.indicator == 3:
                self.gridLayout.addWidget(self.imageLabel3)

        computerVision_BP.fiberfit_model.main(self)
        self.isStarted = True
        self.processImages()
        self.gridLayout.addWidget(self.imageLabel)
        self.indicator = 0


    def nextImage(self):
        self.indicator += 1

        if (self.indicator > 3):
            self.indicator = 0 # reset to zero
            self.gridLayout.removeWidget(self.imageLabel3)
            self.processImages()
            self.gridLayout.addWidget(self.imageLabel)
        if self.indicator == 1:
            self.gridLayout.removeWidget(self.imageLabel)
            self.processImages()
            self.gridLayout.addWidget(self.imageLabel1)
        elif self.indicator == 2:
            self.gridLayout.removeWidget(self.imageLabel1)
            self.processImages()
            self.gridLayout.addWidget(self.imageLabel2)
        elif self.indicator == 3:
            self.gridLayout.removeWidget(self.imageLabel2)
            self.processImages()
            self.gridLayout.addWidget(self.imageLabel3)

    def prevImage(self):
        self.indicator -= 1

        if self.indicator < 0:
            self.indicator = 3 # resest from other end
            self.gridLayout.removeWidget(self.imageLabel)
            self.gridLayout.addWidget(self.imageLabel3)

        if self.indicator == 0:
            self.gridLayout.removeWidget(self.imageLabel1)
            self.processImages()
            self.gridLayout.addWidget(self.imageLabel)
        elif self.indicator == 1:
            self.gridLayout.removeWidget(self.imageLabel2)
            self.processImages()
            self.gridLayout.addWidget(self.imageLabel1)
        elif self.indicator == 2:
            self.gridLayout.removeWidget(self.imageLabel3)
            self.processImages()
            self.gridLayout.addWidget(self.imageLabel2)





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


