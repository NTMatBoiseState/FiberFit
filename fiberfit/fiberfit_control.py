#!/usr/local/bin/python3

"""This is a control part of the GUI application"""

import sys
import csv
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
    results = open('test.csv', 'a') #All instances would have this as a starter. Initialized later in code.

    def __init__(self, Parent = None):
        super(fft_mainWindow, self).__init__()
        self.imgList = []
        self.csvIndex = 0
        self.dataList = []
        self.setupUi(self)
        self.numImages = 0
        self.currentIndex = 0
        self.isStarted = False
        self.canvasExists = False
        self.filename = []
        self.firstOne = True
        self.canvas = None
        #All the events happen below
        self.startButton.clicked.connect(self.start)
        self.nextButton.clicked.connect(self.nextImage)
        self.prevButton.clicked.connect(self.prevImage)
        self.loadButton.clicked.connect(self.launch)
        self.clearButton.clicked.connect(self.clear)
        self.exportButton.clicked.connect(self.export)

    def clear(self):
        self.figureFrame.hide()
        self.kLabel.setText(" ")
        self.muLabel.setText(" ")

    def launch(self):
        dialog = QFileDialog()
        self.filename = dialog.getOpenFileNames(self, '', None) #creates a list of fileNames

    def processImages(self):
        for i in range (0, len(self.filename[0])):
            # trick here is that getOpenFileNames creates a 2D list where the first element of first list is
            # a list of all the selected files. So, I am looping through this first element (0) and through each character
            # of this first element
            th, k, fig = computerVision_BP.process_image(self.filename[0][i])
            name = self.filename[0][i].lstrip('/Users/azatulepbergenov/PycharmProjects/fiberfit/test/')
            #creates a class imgModel and appends to the list of all images
            processedImage = img_model.imgModel(name,th[0],k, fig)
            if (self.firstOne):
                self.imgList.append(processedImage)
                self.numImages += 1
                self.firstOne = False
            for index in range(0, len(self.imgList)): # O(n^2) Yikes!!!
                if (processedImage.getName() == self.imgList[index].getName()):
                    processedImage.setUsed(True)
            if (processedImage.getUsed() != True):
                self.imgList.append(processedImage)
                self.numImages += 1
            else:
                #TODO: Hm, decrements current index on how much there are stuff in a filename array. Not good. Decrements
                #TODO: current index down to 0.
                self.currentIndex -= 1
        if self.isStarted:
            self.gridLayout.removeWidget(self.canvas)
        print(str(self.currentIndex))
        self.canvas = FigureCanvas((self.imgList[self.currentIndex].getFig())) # works!;-)
        self.gridLayout.addWidget(self.canvas)
        self.isStarted = True
        self.figureFrame.show()

    def start(self):
        # sets the current index to the numImages before numImages get updated.
        #Allows consistent use of numImages and the current index value used to
        #access elements in a list.
        self.currentIndex = self.numImages
        self.processImages()
        self.setupLabels(self.currentIndex)

    def setupLabels(self, num):
        self.kLabel.setText("k = " + str(round(self.imgList[num].getK(),2)))
        self.muLabel.setText("mu = " + str(round(self.imgList[num].getTh(),2)))

    def nextImage(self):
        if (self.isStarted):
            image = self.imgList[(self.currentIndex + 1)%len(self.imgList)]
            self.gridLayout.removeWidget(self.canvas)
            self.canvas = FigureCanvas(image.getFig())
            self.gridLayout.addWidget(self.canvas)
            self.setupLabels((self.currentIndex + 1)%len(self.imgList))
            self.currentIndex += 1

    def prevImage(self):
        if (self.isStarted):
            image = self.imgList[(self.currentIndex - 1)%len(self.imgList)]
            self.gridLayout.removeWidget(self.canvas)
            self.canvas = FigureCanvas(image.getFig())
            self.gridLayout.addWidget(self.canvas)
            self.setupLabels((self.currentIndex + 1)%len(self.imgList))
            self.currentIndex -= 1

    def export(self):
        for i in range (self.csvIndex, self.numImages):
            self.dataList.append([self.imgList[i].getName(), self.imgList[i].getTh(), self.imgList[i].getK()])
            self.csvIndex += 1
        with open('test.csv', 'w') as fp:
            a = csv.writer(fp)
            a.writerows(self.dataList)
      #Thing works, but need to think of how to empty the dataList after one use, so that the file will not get overwritten with the same stuff
      #multiple times...


app = QtWidgets.QApplication(sys.argv)
fft_app = fft_mainWindow()
fft_app.show()
sys.exit(app.exec_())


