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

class fft_mainWindow(fiberfit_GUI.Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self, Parent = None):
        super(fft_mainWindow, self).__init__()
        self.setupUi(self)
        #self.indicator = 0 #which image?
        self.numImages = 0
        self.isStarted = False
        self.startButton.clicked.connect(self.start)
        #self.nextButton.clicked.connect(self.nextImage)
        #self.prevButton.clicked.connect(self.prevImage)
        self.loadButton.clicked.connect(self.launch)

    def launch(self):
        dialog = QFileDialog()
        #dialog.setWindowTitle("Select image")
        #dialog.setNameFilter("Images (*.png)")
        #dialog.setFileMode(QFileDialog.ExistingFile)
        #if dialog.exec_() == QtWidgets.QDialog.Accepted:
        #    self.filename = dialog.selectedFiles()[0]

        #Didn't work this way --> fix it later...
        self.filename = dialog.getOpenFileName(self, 'Select Image', '', None) #creates a list of fileNames
        #print (self.filename[0]) for debugging

    def processImages(self):
        self.image = QPixmap("image" + str(self.numImages));
        #label = "image" + str(self.numImages) #for debug
        #print(label)  for debugging
        self.imageLabel = QtWidgets.QLabel()
        self.imageLabel.setPixmap(self.image)
        self.imageLabel.setScaledContents(True)
        self.numImages += 1

    def start(self): #fix the restart option
        if (self.isStarted):
            self.gridLayout.removeWidget(self.imageLabel)
        computerVision_BP.fiberfit_model.main(self, self.filename[0])
        self.processImages()
        self.gridLayout.addWidget(self.imageLabel)
        self.isStarted = True

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


