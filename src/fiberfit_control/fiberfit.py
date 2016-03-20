#!/usr/local/bin/python3

"""This is a control part of the GUI application"""


"3rd party imports: "
import pathlib
import sys
import datetime
import matplotlib
import threading
import time
matplotlib.use("Qt5Agg")  # forces to use Qt5Agg so that Backends work
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtWidgets
from PyQt5.Qt import *
from PyQt5.QtWidgets import QFileDialog  # In order to select a file
from orderedset import OrderedSet
import base64
from PyQt5.QtCore import pyqtSlot, pyqtSignal
import os
from PyQt5.QtWidgets import QDesktopWidget
import random
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import shutil

"custom file imports"
from src.fiberfit_control.support import my_exception as MyException
from src.fiberfit_gui import fiberfit_GUI
from src.fiberfit_model import computerVision_BP
from src.fiberfit_control.support import img_model
from src.fiberfit_control.support import settings
from src.fiberfit_control.support import error
from src.fiberfit_control.support import report

"""
Main window of the application
"""
class fft_mainWindow(fiberfit_GUI.Ui_MainWindow, QtWidgets.QMainWindow):
    show_report = pyqtSignal(int)
    make_report = pyqtSignal(img_model.ImgModel)
    do_run = pyqtSignal()
    do_update = pyqtSignal(int)
    sendProcessedImagesList = pyqtSignal(list, list, OrderedSet, float, float, float, float)
    #  For pbar
    sendProcessedImageCounter = pyqtSignal(int, img_model.ImgModel, list, int, int, int)
    #  Error sig
    sendErrorSig = pyqtSignal(list, int, int)

    """
    Initializes all instance variables a.k.a attributes of a class.
    """

    def __init__(self, Parent=None):
        super(fft_mainWindow, self).__init__()
        # screen dim
        self.screenDim, self.dpi = self.receiveDim()
        self.imgList = OrderedSet()
        self.csvIndex = 0
        self.dataList = []
        self.setupUi(self, self.screenDim.height(), self.screenDim.width())
        self.currentIndex = 0
        self.isStarted = False
        self.filenames = []
        self.firstOne = True
        # dir
        self.directory = None
        # Canvases to display the figures.
        self.imgCanvas = None
        self.logSclCanvas = None
        self.angDistCanvas = None
        self.cartDistCanvas = None
        self.runtime = 0
        self.isResized = False
        # Pops up a dialog with
        self.dialogTextBrowser = report.ReportDialog(self, self.screenDim)
        self.settingsBrowser = settings.SettingsWindow(self, self.screenDim)
        self.errorBrowser = error.ErrorDialog(self, self.screenDim)
        # Settings
        self.uCut = float(self.settingsBrowser.ttopField.text())
        self.lCut = float(self.settingsBrowser.tbottomField.text())
        self.angleInc = float(self.settingsBrowser.btopField.text())
        self.radStep = float(self.settingsBrowser.bbottomField.text())
        # dataList for export
        self.dataList = []
        # All the events happen below
        self.startButton.clicked.connect(self.start)
        self.nextButton.clicked.connect(self.nextImage)
        self.prevButton.clicked.connect(self.prevImage)

        self.loadButton.clicked.connect(self.launch)

        self.do_update.connect(self.populateComboBox)
        self.do_update.connect(self.setupLabels)

        self.clearButton.clicked.connect(self.clear)
        self.exportButton.clicked.connect(lambda i: self.show_report.emit(self.currentIndex))

        # self.make_report.connect(self.dialogTextBrowser.printerSetup)
        self.show_report.connect(self.do_show_report)
        self.make_report.connect(self.dialogTextBrowser.do_test)

        # sends export data sets
        self.sendProcessedImagesList.connect(self.dialogTextBrowser.receiver)

        self.settingsButton.clicked.connect(self.settingsBrowser.do_change)
        self.settingsBrowser.sendValues.connect(self.updateValues)

        # sends off a signal containing string.
        # Conveniently the string will be the name of the file.
        self.selectImgBox.activated[str].connect(self.changeState)

        # pbar
        self.do_run.connect(self.runner)
        self.progressBar.setMinimum(0)
        self.sendProcessedImageCounter.connect(self.processImages)

        self.number = 0 # I need it to be able to process multiple images.

        self.sendErrorSig.connect(self.handleError)
        # self.initialize()

        """This is to gain better insight into Slots and Signals.
        def userLog(int):
            print("User requested reported for image: {}".format(int))
        self.show_report.connect(userLog)
        """

    def initialize(self):
        directory = "temp"
        isCreated = False
        while isCreated == False:
            randomNum = random.randint(0, 100000000) # 10,000,000
            self.directory = directory+randomNum.__str__()
            print("I created dir!")
            if not os.path.exists(directory):
                os.makedirs(self.directory)
                isCreated = True
                print("wtf....")

    """
    Updates the settings
    """
    @pyqtSlot(float, float, float, float)
    def updateValues(self, uCut, lCut, angleInc, radStep):
        self.uCut = uCut
        self.lCut = lCut
        self.angleInc = angleInc
        self.radStep = radStep

    @pyqtSlot(list, int, int)
    def handleError(self, files, index, identifier):
        if identifier == 0:
            self.errorBrowser.label.setText("""ERROR:

            Sorry, unfortunately, this file - {name} can not be processed.

            Please make sure that the image has 8-bit image depth,or, equivalently, gray color space and verify that you are using one of the approved file formats: pdf, png, tif, gif, or bmp."""
                                            .format(name=files[index]))
        elif identifier == 1:
            self.errorBrowser.label.setText("""ERROR:
Sorry, unfortunately, the setting you selected are out of input domain for FiberFit.
Please go back to "Settings" and change some values.
            """
                                            )
        else:
            self.errorBrowser.label.setText("""ERROR:

            Sorry, unforutnately, this file - {name} can not be processed.

            Please make sure that the image is square. """.format(name=files[index]))
        self.errorBrowser.show()
        self.progressBar.hide()


    def runner(self):
        # for filename in self.filenames:
        #           # Retrieve Figures from data analysis code
        #     try:
        #         sig, k, th, R2, angDist, cartDist, logScl, orgImg,  figWidth, figHeigth = computerVision_BP.process_image(filename,
        #                                                                                              self.uCut,
        #                                                                                              self.lCut, self.angleInc,
        #                                                                                              self.radStep, self.screenDim,
        #                                                                                              self.dpi)
        #     except TypeError:
        #         self.errorBrowser.show()
        #     except ValueError:
        #         self.errorBrowser.show()
        #     except OSError:
        #         self.errorBrowser.show()


        pThread = myThread(self.sendProcessedImageCounter, self.sendErrorSig, self.progressBar, self.errorBrowser, self.directory, self.number)
        pThread.update_values(self.uCut, self.lCut, self.angleInc, self.radStep, self.screenDim, self.dpi, self.filenames)
        if (self.filenames.__len__() != 0):
            self.progressBar.show()
            self.progressBar.setValue(0)
        a = pThread.start()


    """
    Function that signals to show the report.
    """

    def do_show_report(self):
        if (self.isStarted):
            self.make_report.emit(self.imgList[self.currentIndex%self.filenames.__len__()])

    """
    Calculates dimensions of the screen.
    """

    def receiveDim(self):
        screenDim = QDesktopWidget().availableGeometry()
        screen = QtWidgets.QApplication.primaryScreen()
        dpi = screen.logicalDotsPerInch()
        return screenDim, dpi

    """
    Clears out canvas.
    """

    def clear(self):
        if (self.isStarted):
            self.kLabel.setText("k = ")
            self.muLabel.setText("μ =  ")
            self.RLabel.setText(('R' + u"\u00B2") + " = ")
            self.sigLabel.setText("σ = ")
            # clears canvas
            self.cleanCanvas()
            self.progressBar.hide()
            self.filenames.clear()
            # clears combo-box
            self.selectImgBox.clear()
            # resets isStarted
            self.isStarted = False
            self.dataList.clear()
            # empties all images
            self.imgList.clear()
            # resets current index
            self.currentIndex = 0
            shutil.rmtree(self.directory)
            self.directory = None
            self.number = 0
            print("TOTAL it took {n} seconds.".format(n = self.runtime))

    """
    Allows user to select image to use.
    """

    def launch(self):
        if (self.directory == None):
            self.initialize()
        self.filenames = []
        dialog = QFileDialog()
        filenames = dialog.getOpenFileNames(self, '', None)  # creates a list of fileNames
        for name in filenames[0]:
            self.filenames.append(pathlib.Path(name))
        self.progressBar.setMaximum(len(filenames[0]))
        #self.currentIndex = 0
        self.do_run.emit()


    """
    Processes selected images. Displays it onto a canvas.
    Technical: Creates img_model objects that encapsulate all of the useful data.
    """

    @pyqtSlot(int, img_model.ImgModel, list, int, int, int)
    def processImages(self, count, processedImage, processedImagesList, isLast, time, number):
        self.number = number
        # Ordered Set
        if processedImage in self.imgList:
            print("Before removing : " + str(self.imgList.__len__()))
            self.imgList.remove(processedImage)
            print("After removing : " + str(self.imgList.__len__()))
            self.imgList.add(processedImage)
            print("After addubg : " + str(self.imgList.__len__()))
            #self.currentIndex -= 1
        else:
            self.imgList.add(processedImage)
            print("I addded this image")
        self.sendProcessedImagesList.emit(processedImagesList, self.dataList, self.imgList, self.uCut, self.lCut, self.radStep,
                                          self.angleInc)

        if self.isStarted:
            # removes/deletes all canvases
            self.cleanCanvas()
        # fills canvas
        print("FOFODF" + str(self.imgList.__len__()))
        print("SODSD" + str(self.currentIndex))
        try:
            self.fillCanvas(self.imgList.__getitem__(self.currentIndex))
        except IndexError:
            self.currentIndex -= 1
            self.fillCanvas(self.imgList.__getitem__(self.currentIndex))
        print("DID I EXCUTE RIGHT AMOUNT OF TIMES?")
        if (not self.isResized):
            self.applyResizing()
            self.isResized = True
        # started
        self.isStarted = True
        self.do_update.emit(self.currentIndex)
        self.removeTemp()
        #  Setting progress bar business
        self.progressBar.setValue(count)
        self.progressBar.valueChanged.emit(self.progressBar.value())
        self.currentIndex += 1
        self.runtime += time
        if (isLast == 1):
            #self.currentIndex -= 1
            print("I AM LAST!")


    """
    Makes so that screen can be resized after the images loaded.
    """

    def applyResizing(self):
        self.resize(0.7 * self.screenDim.height(), 0.8 *self.screenDim.height())
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.figureWidget.sizePolicy().hasHeightForWidth())
        self.figureWidget.setSizePolicy(sizePolicy)

    """
    Populates combox box with the names.
    """

    @pyqtSlot()
    def populateComboBox(self):
        self.selectImgBox.clear()
        for element in self.imgList:
            self.selectImgBox.addItem(element.filename.stem)
        self.selectImgBox.setCurrentIndex(self.currentIndex)

    """
    Cleans the canvas.
    """

    def cleanCanvas(self):
        self.figureLayout.removeWidget(self.angDistCanvas)
        self.figureLayout.removeWidget(self.cartDistCanvas)
        self.figureLayout.removeWidget(self.logSclCanvas)
        self.figureLayout.removeWidget(self.imgCanvas)
        self.angDistCanvas.deleteLater()
        self.cartDistCanvas.deleteLater()
        self.imgCanvas.deleteLater()
        self.logSclCanvas.deleteLater()

    """
    Fills the canvas.
    """

    def fillCanvas(self, img):
        # updates canvases
        self.imgCanvas = QtWidgets.QLabel()
        w = self.imgCanvas.height()
        h = self.imgCanvas.width()
        #use full ABSOLUTE path to the image, not relative
        self.imgCanvas.setPixmap(QPixmap(self.directory + "/orgImg_" + img.number.__str__() + ".png").scaled(300,400,Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.imgCanvas.setScaledContents(True)
        self.imgCanvas.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)



        self.logSclCanvas = QtWidgets.QLabel()
        self.logSclCanvas.setPixmap(QPixmap(self.directory + "/logScl_" + img.number.__str__() + ".png").scaled(300,400,Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logSclCanvas.setScaledContents(True)
        self.logSclCanvas.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)

        self.angDistCanvas = QtWidgets.QLabel()
        self.angDistCanvas.setPixmap(QPixmap(self.directory + "/angDist_" + img.number.__str__() + ".png").scaled(300,400,Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.angDistCanvas.setScaledContents(True)
        self.angDistCanvas.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)

        self.cartDistCanvas = QtWidgets.QLabel()
        self.cartDistCanvas.setPixmap(QPixmap(self.directory + "/cartDist_" + img.number.__str__() + ".png").scaled(300,400,Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.cartDistCanvas.setScaledContents(True)
        self.cartDistCanvas.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)


        #self.imgCanvas = FigureCanvas(img.orgImg)
        #self.logSclCanvas = FigureCanvas(img.logScl)
        #self.angDistCanvas = FigureCanvas(img.angDist)
        #self.cartDistCanvas = FigureCanvas(img.cartDist)
        # adds them to layout
        self.figureLayout.addWidget(self.imgCanvas, 0, 0)
        self.figureLayout.addWidget(self.logSclCanvas, 0, 1)
        self.figureLayout.addWidget(self.angDistCanvas, 1, 0)
        self.figureLayout.addWidget(self.cartDistCanvas, 1, 1)
        self.figureLayout.itemAtPosition(0, 1).widget().setToolTip("FFT Power Spectrum")
        self.figureLayout.itemAtPosition(0, 0).widget().setToolTip("Analyzed Image")
        self.figureLayout.itemAtPosition(1, 0).widget().setToolTip("Red Line = Fiber Orientation")
        self.figureLayout.itemAtPosition(1, 1).widget().setToolTip("Blue Line = Fiber Distribution")
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
        # Processes selected images; sets up the labels and fills selectImgBox with references to images.
        # TODO: Make an exception to catch IndexError, and pop the window with appropriate message.
        self.kLabel.setText("k = ")
        self.muLabel.setText("μ =  ")
        self.RLabel.setText(('R' + u"\u00B2") + " = ")
        self.sigLabel.setText("σ = ")
        # clears canvas
        self.cleanCanvas()
        # clears combo-box
        self.selectImgBox.clear()
        # resets isStarted
        self.isStarted = False
        # empties all images
        self.imgList.clear()
        # resets current index
        self.currentIndex = 0
        self.do_run.emit()
        #self.do_update.emit(self.currentIndex)
        self.removeTemp()

    """
    Removes files in temp directory. Prevents memory leak.
    """

    def removeTemp(self):
        # TODO: fix bug so that it does remove images only when they are selected.
        files = []
        files.append('angDist.png')
        files.append('orgImg.png')
        files.append('cartDist.png')
        files.append('logScl.png')
        files.append('angDist4.png')
        files.append('orgImg4.png')
        files.append('cartDist4.png')
        files.append('logScl4.png')
        for filename in files:
            if os.path.isfile(filename):
                os.remove(filename)

    """
    Sets up appropriate labels depending on which image is selected.
    """

    @pyqtSlot(int)
    def setupLabels(self, num):
        self.sigLabel.setText("σ = " + str(round(self.imgList.__getitem__(num).sig[0], 2)))
        self.kLabel.setText("k = " + str(round(self.imgList.__getitem__(num).k, 2)))
        self.muLabel.setText("μ = " + str(round(self.imgList.__getitem__(num).th, 2)))
        self.RLabel.setText(('R' + u"\u00B2") + " = " + str(round(self.imgList.__getitem__(num).R2, 2)))

    """
    Scrolls to next image.
    Uses a circular array as an underlying data structure. Main advantage is
    access by index; that is eliminate unnecessary search for item.
    """

    def nextImage(self):
        if (self.isStarted):
            # updates current index
            self.currentIndex = (self.currentIndex + 1) % len(self.imgList)
            image = self.imgList.__getitem__(self.currentIndex)
            self.cleanCanvas()
            self.fillCanvas(image)
            self.setupLabels((self.currentIndex))
            self.selectImgBox.setCurrentIndex(self.currentIndex)

    """
    Scrolls to previous image.
    Uses a circular array as an underlying data structure. Main advantage is
    access by index; that is eliminate unnecessary search for item.
    """

    def prevImage(self):
        if (self.isStarted):
            # updates current index
            self.currentIndex = (self.currentIndex - 1) % len(self.imgList)
            image = self.imgList.__getitem__(self.currentIndex)
            self.cleanCanvas()
            self.fillCanvas(image)
            self.setupLabels(self.currentIndex)
            self.selectImgBox.setCurrentIndex(self.currentIndex)

    """
    Slot for Combo Box's activated() signal. Searches for image and displays it onto
    canvas.
    Note, O(n) because of performing a search for image.
    """

    def changeState(self, filename):
        # find img
        for image in self.imgList:
            if image.filename.stem == filename:
                self.processImagesFromComboBox(image)
                self.sigLabel.setText("σ = " + str(round(image.sig[0], 2)))
                self.kLabel.setText("k = " + str(round(image.k, 2)))
                self.muLabel.setText("μ = " + str(round(image.th, 2)))
                self.RLabel.setText(('R' + u"\u00B2") + " = " + str(round(image.R2, 2)))
                # sets current index to the index of the found image.
                self.currentIndex = self.imgList.index(image)


    def closeEvent(self, event):
        self.delete_dir(self.directory)


    def delete_dir(self, dir):
        import shutil
        try:
            shutil.rmtree(dir)
        except:
            pass
            # means direcotry has not been created. if usre opens an app and then immediately closes it.


class myThread(threading.Thread):


    def __init__(self, sig, errorSig, bar, errorBrowser, dir, num):
        super(myThread, self).__init__()
        self.uCut = 0
        self.lCut = 0
        self.angleInc = 0
        self.radStep = 0
        self.screenDim = 0
        self.dpi = 0
        self.sig = sig
        self.filenames = []
        self.bar = bar
        self.errorBrowser = errorBrowser
        self.errorSig = errorSig
        self.directory = dir
        self.number = num


    def update_values(self, uCut, lCut, angleInc, radStep, screenDim, dpi, filenames):
        self.lCut = lCut
        self.uCut = uCut
        self.angleInc = angleInc
        self.radStep = radStep
        self.screenDim = screenDim
        self.dpi = dpi
        self.filenames = filenames

    def run(self):
        processedImagesList = []
        count = 0
        toContinue = True
        start = time.time()
        isZeroException = 0
        print(start)
        isLast = 0
        for filename in self.filenames:
            toContinue = True
            #start = time.time()

            # Retrieve Figures from data analysis code
            try:
                sig, k, th, R2, angDist,  cartDist, logScl,  orgImg,  figWidth, figHeigth, runtime = computerVision_BP.process_image(filename,
                                                                                               self.uCut,
                                                                                               self.lCut, self.angleInc,
                                                                                               self.radStep, self.screenDim,
                                                                                               self.dpi,
                                                                                               self.directory,
                                                                                               self.number)

                # Starting from Python3, there is a distinctin between bytes and str. Thus, I can't use
                # methods of str on bytes. However I need to do that in order to properly encode the image
                # into b64. The main thing is that bytes-way produces some improper characters that mess up
                # the decoding process. Hence, decode(utf-8) translates bytes into str.

                angDistEncoded = base64.encodebytes(open(self.directory + "/" + 'angDist_' + self.number.__str__() + '.png', 'rb').read()).decode('utf-8')
                cartDistEncoded = base64.encodebytes(open(self.directory + "/" + 'cartDist_' + self.number.__str__() + '.png', 'rb').read()).decode('utf-8')
                logSclEncoded = base64.encodebytes(open(self.directory + "/" + 'logScl_' + self.number.__str__() + '.png', 'rb').read()).decode('utf-8')
                orgImgEncoded = base64.encodebytes(open(self.directory + "/" +  'orgImg_' + self.number.__str__() + '.png', 'rb').read()).decode('utf-8')
                #
                # angDistEncoded4 = base64.encodebytes(open('angDist4.png', 'rb').read()).decode('utf-8')
                # cartDistEncoded4 = base64.encodebytes(open('cartDist4.png', 'rb').read()).decode('utf-8')
                # logSclEncoded4 = base64.encodebytes(open('logScl4.png', 'rb').read()).decode('utf-8')
                # orgImgEncoded4 = base64.encodebytes(open('orgImg4.png', 'rb').read()).decode('utf-8')

                # Creates an object
                processedImage = img_model.ImgModel(
                    filename=filename,
                    sig = sig,
                    k=k,
                    th=th,
                    R2=R2,
                    orgImg=orgImg,
                    orgImgEncoded=orgImgEncoded,
                   # orgImg4=orgImg4,
                   # orgImgEncoded4 = orgImgEncoded4,
                    logScl=logScl,
                    logSclEncoded=logSclEncoded,
                   # logScl4 = logScl4,
                   # logSclEncoded4 = logSclEncoded4,
                    angDist=angDist,
                    angDistEncoded=angDistEncoded,
                   # angDist4 = angDist4,
                   # angDistEncoded4 = angDistEncoded4,
                    cartDist=cartDist,
                    cartDistEncoded=cartDistEncoded,
                   # cartDist4 = cartDist4,
                   # cartDistEncoded4 = cartDistEncoded4,
                    timeStamp= datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"),
                    number= self.number)
                self.number += 1
                processedImagesList.append(processedImage)
                count += 1
                if (count == len(self.filenames)):
                    isLast = 1

            except MyException.MyError:
                toContinue = False;
                isZeroException = 2

            except TypeError:
                print("typeerror")

                toContinue = False
            except ValueError:
                print("ValueError")

                toContinue = False
            except OSError:
                print("OSErrro in thread")
                toContinue = False

            except ZeroDivisionError:
                toContinue = False
                isZeroException = 1

            #except:
            #    toContinue = False
            #    isZeroException = 1

            finally:
                if (toContinue):
                    self.sig.emit(count, processedImage, processedImagesList, isLast, runtime, self.number)
                else:
                    print("I am in else")
                    self.errorSig.emit(self.filenames, count, isZeroException)
        end = time.time()

        print(end)
        print(start)
        print(end - start)
        if toContinue:
            time.sleep(0.5)
            self.bar.setWindowOpacity(0)
            self.bar.hide()
def main():
    """
    Enters an event-loop.
    """
    app = QtWidgets.QApplication(sys.argv)
    fft_app = fft_mainWindow()
    fft_app.receiveDim()
    #delete_dir(dir)
    fft_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
