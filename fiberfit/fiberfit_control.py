#!/usr/local/bin/python3

"""This is a control part of the GUI application"""
import os
import pathlib
import glob
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
from orderedset import OrderedSet
from PyQt5.QtWidgets import QFileSystemModel

class fft_mainWindow(fiberfit_GUI.Ui_MainWindow, QtWidgets.QMainWindow):
    results = open('test.csv', 'a') #All instances would have this as a starter. Initialized later in code.

    """
    Initializes all instance variables a.k.a attributes of a class.
    """
    def __init__(self, Parent = None):
        super(fft_mainWindow, self).__init__()
        self.imgList = OrderedSet()
        self.csvIndex = 0
        self.dataList = []
        self.setupUi(self)
        self.numImages = 0
        self.currentIndex = 0
        self.dialog = QFileDialog()
        self.isStarted = False
        self.canvasExists = False
        self.filenames = []
        self.firstOne = True
        self.imgCanvas = None
        self.logSclCanvas = None
        self.angDistCanvas = None
        self.cartDistCanvas = None
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
        fileMod = QFileSystemModel()
        fileMod.setRootPath('~')
        view = QtWidgets.QTreeView()
        view.setModel(fileMod)
        #view.show()
        dialog = QtWidgets.QDialog()

        dialog.exec()

        self.gridLayout2 = QtWidgets.QGridLayout(dialog)
        self.gridLayout2.addWidget(view)
        self.filenames = fileMod.fileName()
        print(self.filenames)





        #self.dialog.
        #self.dialog.setFileMode(self.dialog.ExistingFiles)-
        #self.dialog.directoryEntered.connect(self.getFromDir)
        #self.dialog.filesSelected.connect(self.getFromFile)
        print(self.filenames)




        #if ():
        #    filenames = dialog.getOpenFileNames(self, '', None) #creates a list of fileNames
        #else:
        #    filenamesDir = dialog.getExistingDirectory()
        #    flag = False
        #print(filenames)
        #print(filenamesDir)


        #self.filenames = []
        #for file in filenames[0]:
        #    if file.is_dir():
        #        # TODO: find all files in dir
        #        self.filenames.append(  )
        #    else:
        #        self.filenames.append( pathlib.Path(file) )


    def getFromFile(self):
        filenames = self.dialog.getOpenFileNames(self, '', None)
        for i in range (0, len(filenames[0])):
            self.filenames.append(filenames[i])

    def getFromDir(self):
        filenamesDir = self.dialog.getExistingDirectory()
        os.chdir(filenamesDir)
        self.filenames = glob.glob('*.png')

    """
    Processes selected images. Displays it onto a canvas.
    Technical: Creates img_model objects that encapsulate all of the useful data.
    """
    #@PyQt.Slot(List)
    def processImages(self, filenames):

        for filename in filenames:
            # Retrieve Figures from data analysis code
            k, th, fig, angDist, cartDist, logScl, orgImg = computerVision_BP.process_image(filename)

            # Stores the PathName, so that it can be trimmed off the filename.
            name = filename.name

            # Creates a class imgModel and appends to the list of all images
            processedImage = img_model.ImgModel(
                filename=name,
                k=k[0],
                th=th,
                figure=fig,
                orgImg=orgImg,
                logScl=logScl,
                angDist=angDist,
                cartDist=cartDist,
                timeStamp=datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"))

            self.imgList.add(processedImage)
            self.selectImgBox.addItem(processedImage.getName())
            # TODO: use OrderedSet (need to implement __eq__ and/or __hashcode__, see SO)

        if (self.currentIndex == len(self.imgList)):
            self.currentIndex -= 1

        if self.isStarted:
            # removes/deletes all canvases
            self.cleanCanvas()

        #fills canvas
        # TODO: send as signal!
        # example:
        #     self.updateCanvasSignal.emit(self.currentIndex)
        self.fillCanvas(self.imgList[self.currentIndex])

        #started
        self.isStarted = True


    def cleanCanvas(self):
        self.figureLayout.removeWidget(self.angDistCanvas)
        self.figureLayout.removeWidget(self.cartDistCanvas)
        self.figureLayout.removeWidget(self.logSclCanvas)
        self.figureLayout.removeWidget(self.imgCanvas)
        self.angDistCanvas.deleteLater()
        self.cartDistCanvas.deleteLater()
        self.imgCanvas.deleteLater()
        self.logSclCanvas.deleteLater()

    def fillCanvas(self, img):
        #updates canvases
        self.imgCanvas = FigureCanvas(img.getOriginalImg())
        self.logSclCanvas = FigureCanvas(img.getLogScl())
        self.angDistCanvas = FigureCanvas(img.getAngDist())
        self.cartDistCanvas = FigureCanvas(img.getCartDist())
        #adds them to layout
        self.figureLayout.addWidget(self.imgCanvas, 0, 0)
        self.figureLayout.addWidget(self.logSclCanvas, 0, 1)
        self.figureLayout.addWidget(self.angDistCanvas, 1, 0)
        self.figureLayout.addWidget(self.cartDistCanvas, 1, 1)

    """
    Helps to process an image from using a Combo Box.
    @param: img to be processed
    """
    def processImagesFromComboBox(self, img):
        if self.isStarted:
            self.cleanCanvas()
        self.fillCanvas(img)

    """
    Starts the application.
    """
    def start(self):
        # sets the current index to the numImages before numImages get updated.
        #Allows consistent use of numImages and the current index value used to
        #access elements in a list.
        self.currentIndex = len(self.imgList)
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
            self.cleanCanvas()
            self.fillCanvas(image)
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
            self.cleanCanvas()
            self.fillCanvas(image)
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
            a.writerow(['Name', 'Th', 'K', 'Time'])
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


