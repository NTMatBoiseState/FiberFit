#!/usr/local/bin/python3

"""This is a control part of the GUI application"""

import sys
import matplotlib
matplotlib.use("Qt5Agg") ## forces to use Qt5Agg so that Backends work
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from fiberfit import fiberfit_GUI
from fiberfit import computerVision_BP
from PyQt5 import QtWidgets
from PyQt5.Qt import*
from PyQt5.QtWidgets import QFileDialog
from fiberfit import img_model

class fft_mainWindow(fiberfit_GUI.Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self, Parent = None):
        super(fft_mainWindow, self).__init__()
        self.imgList = []
        self.setupUi(self)
        self.numImages = 0
        self.isStarted = False
        self.canvasExists = False
        self.filename = None
        self.canvas = None
        self.startButton.clicked.connect(self.start)
        #self.nextButton.clicked.connect(self.nextImage)
        #self.prevButton.clicked.connect(self.prevImage)
        self.loadButton.clicked.connect(self.launch)
        self.clearButton.clicked.connect(self.clear)

    def clear(self):
        self.figureFrame.hide()
        self.kLabel.setText(" ")
        self.muLabel.setText(" ")

    def launch(self):
        dialog = QFileDialog()
        self.filename = dialog.getOpenFileName(self, 'Select Image', '', None) #creates a list of fileNames

    def processImages(self):
        th, k, fig = computerVision_BP.process_image(self.filename[0])
        if self.isStarted:
            self.gridLayout.removeWidget(self.canvas)
        self.imgList.append(img_model.imgModel(th,k)) # works!;-)
        self.canvas = FigureCanvas(fig) # works!;-)
        self.gridLayout.addWidget(self.canvas)
        self.isStarted = True
        self.figureFrame.show()


    def start(self): #fix the restart option
        self.processImages()
        self.kLabel.setText("k = " + str(round(self.imgList[self.numImages].getK(),2)))
        self.muLabel.setText("mu = " + str(round(self.imgList[self.numImages].getTh()[0],2)))
        self.numImages += 1


 # Below this line is stuff not necessary to run the program. Though, it is useful for me as a developer for
 # future.

    def nextImage(self):
        self.indicator += 1

        if (self.indicator > self.increment):
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


app = QtWidgets.QApplication(sys.argv)
fft_app = fft_mainWindow()
fft_app.show()
sys.exit(app.exec_())


