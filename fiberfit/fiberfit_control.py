#!/usr/local/bin/python3

"""This is a control part of the GUI application"""

import sys
import csv
import datetime
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
            processedImage = img_model.imgModel(name,th[0],k, fig, None, datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"))
            #Special case when the image is the first one in the list, then it is by now means a duplicate.
            if (self.firstOne):
                self.imgList.append(processedImage)
                self.numImages += 1
                self.firstOne = False
            #Searches and compares if the processed image is equivalent to any of already added images.
            #If so, then, processedImage has been used.
            for index in range(0, len(self.imgList)): # O(n^2) Yikes!!!
                if (processedImage.getName() == self.imgList[index].getName()):
                    processedImage.setUsed(True)
            #If not used then, I can append processed images to an imgList.
            if (processedImage.getUsed() != True):
                self.imgList.append(processedImage)
                self.numImages += 1
        if (self.currentIndex == self.numImages):
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
        self.kLabel.setText("mu = " + str(round(self.imgList[num].getK(),2)))
        self.muLabel.setText("k = " + str(round(self.imgList[num].getTh(),2)))

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
        #self.dataList.append(['Name', 'Th', 'K', 'Time'])
        for i in range (self.csvIndex, self.numImages):
            self.dataList.append([self.imgList[i].getName(), self.imgList[i].getTh(), self.imgList[i].getK(), self.imgList[i].getTimeStamp()])
            self.csvIndex += 1
        with open('test.csv', 'w') as fp:
            a = csv.writer(fp)
            a.writerow(['Name', 'K', 'Th', 'Time'])
            a.writerows(self.dataList)

app = QtWidgets.QApplication(sys.argv)
fft_app = fft_mainWindow()
fft_app.show()
sys.exit(app.exec_())


