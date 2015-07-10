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
from PyQt5.QtWidgets import QFileDialog #In order to select a file
from PyQt5.QtCore import QFileInfo #In order to get a pathname to a file.
from fiberfit import img_model

#TODO: 1) Eliminate dependency on having a path to file explicitly listed.  DONE.
#TODO: 2) Deal with resizability and making GUI pretty. !!
#TODO: 3) Look into dictionaries. !

class fft_mainWindow(fiberfit_GUI.Ui_MainWindow, QtWidgets.QMainWindow):
    results = open('test.csv', 'a') #All instances would have this as a starter. Initialized later in code.

    """
    Initializes all instance variables a.k.a attributes of a class.
    """
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
        #sends off a signal containing string.
        #Conveniently the string will be the name of the file.
        self.selectImgBox.activated[str].connect(self.changeState)

    """
    Clears out canvas.
    """
    def clear(self):
       # self.figureFrame.hide()
        self.kLabel.setText(" ")
        self.muLabel.setText(" ")

    """
    Allows user to select image to use.
    """
    def launch(self):
        dialog = QFileDialog()
        self.filename = dialog.getOpenFileNames(self, '', None) #creates a list of fileNames

    """
    Processes selected images. Displays it onto a canvas.
    Technical: Creates img_model objects that encapsulate all of the useful data.
    """
    def processImages(self):
        for i in range (0, len(self.filename[0])):
            # trick here is that getOpenFileNames creates a 2D list where the first element of first list is
            # a list of all the selected files. So, I am looping through this first element (0) and through each character
            # of this first element
            th, k, fig = computerVision_BP.process_image(self.filename[0][i])
            #Stores the pathName, so that it can be trimmed off the filename.
            pathName = QFileInfo(self.filename[0][i]).absoluteDir().absolutePath()
            #Trims the path ;-)
            name = self.filename[0][i].lstrip(pathName)
            #creates a class imgModel and appends to the list of all images
            processedImage = img_model.imgModel(name,th[0],k, fig, None, datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"))
            #Special case when the image is the first one in the list, then it is by now means a duplicate.
            if (self.firstOne):
                self.imgList.append(processedImage)
                self.numImages += 1
                self.firstOne = False
                self.selectImgBox.addItem(processedImage.getName())
            #Searches and compares if the processed image is equivalent to any of already added images.
            #If so, then, processedImage has been used.
            for index in range(0, len(self.imgList)): # O(n^2) Yikes!!!
                if (processedImage.getName() == self.imgList[index].getName()):
                    processedImage.setUsed(True)
            #If not used then, I can append processed images to an imgList.
            if (processedImage.getUsed() != True):
                self.imgList.append(processedImage)
                self.numImages += 1
                self.selectImgBox.addItem(processedImage.getName())
        if (self.currentIndex == self.numImages):
            self.currentIndex -= 1
        if self.isStarted:
            self.figureLayout.removeWidget(self.canvas)
            self.canvas.deleteLater()
        self.canvas = FigureCanvas((self.imgList[self.currentIndex].getFig()))
        self.figureLayout.addWidget(self.canvas)
        self.isStarted = True
    """
    Helps to process an image from using a Combo Box.
    @param: img to be processed
    """
    def processImagesFromComboBox(self, img):
        if self.isStarted:
            self.figureLayout.removeWidget(self.canvas)
            self.canvas.deleteLater()
        self.canvas = FigureCanvas((img.getFig()))
        self.figureLayout.addWidget(self.canvas)

    """
    Starts the application.
    """
    def start(self):
        # sets the current index to the numImages before numImages get updated.
        #Allows consistent use of numImages and the current index value used to
        #access elements in a list.
        self.currentIndex = self.numImages
        self.processImages()
        self.setupLabels(self.currentIndex)

    """
    Sets up appropriate labels depending on which image is selected.
    """
    def setupLabels(self, num):
        self.kLabel.setText("k = " + str(round(self.imgList[num].getK(),2)))
        self.muLabel.setText("mu = " + str(round(self.imgList[num].getTh(),2)))

    """
    Scrolls to next image.
    Uses a circular array as an underlying data structure. Main advantage is
    access by index; that is eliminate unnecessary search for item.
    """
    def nextImage(self):
        if (self.isStarted):
            image = self.imgList[(self.currentIndex + 1)%len(self.imgList)]
            self.figureLayout.removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = FigureCanvas(image.getFig())
            self.figureLayout.addWidget(self.canvas)
            self.setupLabels((self.currentIndex + 1)%len(self.imgList))
            self.currentIndex += 1
            #XXX: For debugging: print(str(self.currentIndex))

    """
    Scrolls to previous image.
    Uses a circular array as an underlying data structure. Main advantage is
    access by index; that is eliminate unnecessary search for item.
    """
    def prevImage(self):
        if (self.isStarted):
            image = self.imgList[(self.currentIndex - 1)%len(self.imgList)]
            self.figureLayout.removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = FigureCanvas(image.getFig())
            self.figureLayout.addWidget(self.canvas)
            self.setupLabels((self.currentIndex - 1)%len(self.imgList))
            self.currentIndex -= 1
            #XXX: For Debugging: print(str(self.currentIndex))

    """
    Exports results into a .csv file.
    """
    #TODO: Need to add saving of PDF option.
    def export(self):
        for i in range (self.csvIndex, self.numImages):
            self.dataList.append([self.imgList[i].getName(), self.imgList[i].getTh(), self.imgList[i].getK(), self.imgList[i].getTimeStamp()])
            self.csvIndex += 1
        with open('test.csv', 'w') as csvfile:
            a = csv.writer(csvfile)
            a.writerow(['Name', 'K', 'Th', 'Time'])
            a.writerows(self.dataList)

    """
    Slot for Combo Box's activated() signal. Searches for image and displays it onto
    canvas.
    Note, O(n) because of performing a search for image.
    """
    def changeState(self, filename):
        #find img
        for i in range (0, len(self.imgList)):
            if (self.imgList[i].getName() == filename):
                self.processImagesFromComboBox(self.imgList[i])
                self.kLabel.setText("k = " + str(round(self.imgList[i].getK(),2)))
                self.muLabel.setText("mu = " + str(round(self.imgList[i].getTh(),2)))
                self.currentIndex = i
               #XXX: For Debugging: print(str(self.currentIndex))

"""
Enters an event-loop.
"""
app = QtWidgets.QApplication(sys.argv)
fft_app = fft_mainWindow()
fft_app.show()
sys.exit(app.exec_())


