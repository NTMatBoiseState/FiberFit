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
        self.currentIndex = 0
        self.isStarted = False
        self.canvasExists = False
        self.filename = None
        self.canvas = None
        self.startButton.clicked.connect(self.start)
        self.nextButton.clicked.connect(self.nextImage)
        self.prevButton.clicked.connect(self.prevImage)
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
        self.imgList.append(img_model.imgModel(th,k, fig)) # works!;-)
        self.canvas = FigureCanvas(fig) # works!;-)
        self.gridLayout.addWidget(self.canvas)
        self.isStarted = True
        self.figureFrame.show()


    def start(self): #fix the restart option
        self.processImages()
        self.setupLabels(self.numImages)
        self.currentIndex = self.numImages
        self.numImages += 1

    def setupLabels(self, num):
        self.kLabel.setText("k = " + str(round(self.imgList[num].getK(),2)))
        self.muLabel.setText("mu = " + str(round(self.imgList[num].getTh()[0],2)))

    def nextImage(self):
        if (self.isStarted):
            image = self.imgList[(self.currentIndex + 1)%len(self.imgList)]
            self.gridLayout.removeWidget(self.canvas)
            self.canvas = FigureCanvas(image.getFig())
            self.gridLayout.addWidget(self.canvas)
            self.setupLabels((self.currentIndex + 1)%len(self.imgList))
            self.currentIndex += 1
            print(self.numImages)
            print(len(self.imgList))

    def prevImage(self):
        if (self.isStarted):
            image = self.imgList[(self.currentIndex - 1)%len(self.imgList)]
            self.gridLayout.removeWidget(self.canvas)
            self.canvas = FigureCanvas(image.getFig())
            self.gridLayout.addWidget(self.canvas)
            self.setupLabels((self.currentIndex + 1)%len(self.imgList))
            self.currentIndex -= 1
            print(self.numImages)
            print(len(self.imgList))

app = QtWidgets.QApplication(sys.argv)
fft_app = fft_mainWindow()
fft_app.show()
sys.exit(app.exec_())


