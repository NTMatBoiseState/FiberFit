#!/usr/local/bin/python3

"""This is a control part of the GUI application"""
import pathlib
import sys
import csv
import datetime
import matplotlib

matplotlib.use("Qt5Agg")  ## forces to use Qt5Agg so that Backends work
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from fiberfit import fiberfit_GUI
from fiberfit import computerVision_BP
from PyQt5 import QtWidgets
from PyQt5.Qt import *
from PyQt5.QtWidgets import QFileDialog  # In order to select a file
from fiberfit import img_model
from orderedset import OrderedSet
import base64
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialogButtonBox, QDialog
from fiberfit import SettingsDialog
from fiberfit import ExportDialog
from PyQt5.QtGui import QTextDocument
import os
import time
import glob

class SettingsWindow(QDialog, SettingsDialog.Ui_Dialog):
    genUCut = 2.0
    genLCut = 32.0
    genAngInc = 1.0
    genRadStep = 0.5
    sendValues = pyqtSignal(float, float, float, float)
    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)
        self.setupUi(self)
        self.valuesStack = [(self.genUCut, self.genLCut, self.genAngInc, self.genRadStep)]
        self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.make_change)
        self.buttonBox.button(QDialogButtonBox.Reset).clicked.connect(self.reset_changes)
        self.setupDefaultValues()

    """
    Resets changes to the last saved changes.
    """

    def reset_changes(self):
        self.ttopField.setText(self.valuesStack[self.valuesStack.__len__() - 1][0].__str__())
        self.tbottomField.setText(self.valuesStack[self.valuesStack.__len__() -1][1].__str__())
        self.btopField.setText(self.valuesStack[self.valuesStack.__len__() - 1][2].__str__())
        self.bbottomField.setText(self.valuesStack[self.valuesStack.__len__() - 1][3].__str__())

    """
    Sets up default settings.
    """
    def setupDefaultValues(self):
        self.ttopField.setText(self.genUCut.__str__())
        self.tbottomField.setText(self.genLCut.__str__())
        self.btopField.setText(self.genAngInc.__str__())
        self.bbottomField.setText(self.genRadStep.__str__())

    @pyqtSlot()
    def make_change(self):
        uCut = float(self.ttopField.text())
        lCut = float(self.tbottomField.text())
        angleInc = float(self.btopField.text())
        radStep = float(self.bbottomField.text())
        self.valuesStack.append((uCut, lCut, angleInc, radStep))

        self.sendValues.emit(uCut, lCut, angleInc, radStep)

    @pyqtSlot()
    def do_change(self):
        self.show()

class ReportDialog(QDialog, ExportDialog.Ui_Dialog):
    do_print = pyqtSignal()
    do_excel = pyqtSignal()
    sendDataList = pyqtSignal(list)
    def __init__(self, parent=None):
        super(ReportDialog, self).__init__(parent)
        self.dataList = []
        self.setupUi(self)
        self.document = QTextDocument()
        self.list = []
        self.savedfiles = None
        self.currentModel = None
        # settings
        self.uCut = 0
        self.lCut = 0
        self.angleInc = 0
        self.radStep = 0
        # printer
        self.printer = QPrinter(QPrinter.PrinterResolution)
        # Signals and slots:
        self.do_excel.connect(self.exportExcel)
        self.saveBox.button(QDialogButtonBox.SaveAll).clicked.connect(self.saveas)
        self.saveBox.button(QDialogButtonBox.Save).clicked.connect(self.saveas)
        self.do_print.connect(self.print)
        # self.sendDataList.connect(fft_mainWindow.receiveDataList)

    """Makes excel spreadsheet.
    """
    #TODO: Need to work here!
    @pyqtSlot()
    def exportExcel(self):
        if self.dataList.__len__() == 0:
            self.dataList.append(
                [self.list[0].filename.stem,
                 self.uCut,
                 self.lCut,
                 self.radStep,
                 self.angleInc,
                 self.list[0].th,
                 self.list[0].k,
                 self.list[0].R2,
                 self.list[0].timeStamp])
        # temp = self.list
        temp = []
        for i in range(0, self.list.__len__()):
            temp.append(self.list[i])
        for i in range(0, len(self.dataList)):
            found = False
            for j in range(0, len(temp)):
                # One image from list is at most can equal to one another image from temp
                if found == False and self.dataList[i][0] == temp[j].filename.stem:
                    self.dataList.remove(self.dataList[i])
                    self.dataList.insert(i, [temp[j].filename.stem,
                                             self.uCut,
                                             self.lCut,
                                             self.radStep,
                                             self.angleInc,
                                             temp[j].th,
                                             temp[j].k,
                                             temp[j].R2,
                                             temp[j].timeStamp])
                    temp.remove(temp[j])
                    found = True
        for k in range(0, len(temp)):
            self.dataList.append( [temp[k].filename.stem,
                                   self.uCut,
                                   self.lCut,
                                   self.radStep,
                                   self.angleInc,
                                   round(temp[k].th, 2),
                                   round(temp[k].k, 2),
                                   round(temp[k].R2, 2),
                                   temp[k].timeStamp])
        with open(str(self.savedfiles.parents[0]) + '/summary.csv', 'w') as csvfile:
            a = csv.writer(csvfile)
            a.writerow(['Name', 'LowerCut', 'UpperCut', 'RadialStep', 'AngleIncrement', 'Th', 'K', 'R^2', 'Time'])
            a.writerows(self.dataList)
        fft_mainWindow.dataList = self.dataList

    """
    Pops out a dialog allowing user to select where to save the image.
    """
    @pyqtSlot()
    def saveas(self):
        dialog = QFileDialog()
        if (self.saveBox.button(QDialogButtonBox.Save) == self.sender()):
            self.savedfiles = pathlib.Path(dialog.getSaveFileName(self, "Export", self.currentModel.filename.stem)[0])
        else:
            self.savedfiles = pathlib.Path(dialog.getSaveFileName(self, "Export", "The name of each image selected will be appended to whatever you put in here.")[0])
        self.printerSetup()
        self.do_print.emit()
        self.do_excel.emit()
        # print(self.savedfiles)

    """
    Checks which button sent a signal. Based on that it either prints all images or just a single specific image.
    """

    def print(self):
        if (self.saveBox.button(QDialogButtonBox.SaveAll) == self.sender()):
            print('list before printin is:' + self.list.__str__())
            for model in self.list:
                self.document.setHtml(self.createHtml(model))
                # print(self.savedfiles.parents[0].__str__() + '/' + model.filename.stem + '.pdf') <--- for debugging
                self.printer.setOutputFileName(self.savedfiles.parents[0].__str__() + '/' + self.savedfiles.name + model.filename.stem + '.pdf')
                self.document.print(self.printer)
        elif (self.saveBox.button(QDialogButtonBox.Save) == self.sender()):
            self.document.print(self.printer)

    """
    Sets up default instructions for printer.
    """

    def printerSetup(self):
        self.printer.setPageSize(QPrinter.A4)
        self.printer.setOutputFormat(QPrinter.PdfFormat)
        self.printer.setFullPage(True)
        print(self.savedfiles)
        self.printer.setOutputFileName(str(self.savedfiles))

    """
    Creates html-based report that shows the basic information about the sample.
    """
    def createHtml(self, model):
        #TODO: Cut the images' size down to (250, 250) so that to fit to QTextDocument.
        html = """
        <html>
            <head>
                <link type="text/css" rel="stylesheet" href="ntm_style.css"/>
            </head>
            <body>
                <p> Image Name: {name} </p> <p> mu: {th} </p>
                <p>k: {k} </p>
                <p>R^2: {R2} </p>
                <br>
                <table>
                    <tr>
                        <td> <img src = "data:image/png;base64,{encodedOrgImg}" width = "250", height = "250"/></td>
                        <td> <img src ="data:image/png;base64,{encodedLogScl}" width = "250", height = "250"/></td>
                    </tr>
                    <tr>
                        <td> <img src = "data:image/png;base64,{encodedAngDist}" width = "250", height = "250" /></td>
                        <td> <img src = "data:image/png;base64,{encodedCartDist}" width = "250", height = "250" /></td>
                    </tr>
                </table>
                <p><br><br><br><br>
                    {date}
                </p>
            </body>
        </html>
        """.format(name=model.filename.stem, th= round(model.th, 2),  k= round(model.k, 2), R2 = round(model.R2, 2),
                   encodedOrgImg=model.orgImgEncoded.translate('bn\''),
                   encodedLogScl=model.logSclEncoded.translate('bn\''),
                   encodedAngDist=model.angDistEncoded.translate('bn\''),
                   encodedCartDist=model.cartDistEncoded.translate('bn\''),
                   date=model.timeStamp)
        # print(html)
        print('Set html')
        return html

    """
    Makes report for an image that was active when user pressed Export button.
    """
    @pyqtSlot(img_model.ImgModel)
    def do_test(self, model):
        self.webView.setHtml(self.createHtml(model))
        self.document.setHtml(self.createHtml(model))
        self.currentModel = model
        self.show()

    @pyqtSlot(list, list, float, float, float, float)
    def receiver(self, selectedImgs, dataList, uCut, lCut, radStep, angleInc):
        self.dataList = dataList
        self.list = selectedImgs
        self.uCut = uCut
        self.lCut = lCut
        self.radStep = radStep
        self.angleInc = angleInc

class fft_mainWindow(fiberfit_GUI.Ui_MainWindow, QtWidgets.QMainWindow):
    show_report = pyqtSignal(int)
    make_report = pyqtSignal(img_model.ImgModel, OrderedSet)
    do_run = pyqtSignal()
    do_update = pyqtSignal(int)
    sendProcessedImagesList = pyqtSignal(list, list, float, float, float, float)

    """
    Initializes all instance variables a.k.a attributes of a class.
    """

    def __init__(self, Parent=None):
        super(fft_mainWindow, self).__init__()
        self.imgList = OrderedSet()
        self.csvIndex = 0
        self.dataList = []
        self.setupUi(self)
        self.currentIndex = 0
        self.isStarted = False
        self.filenames = []
        self.firstOne = True
        # Canvases to display the figures.
        self.imgCanvas = None
        self.logSclCanvas = None
        self.angDistCanvas = None
        self.cartDistCanvas = None
        # Pops up a dialog with
        self.dialogTextBrowser = ReportDialog(self)
        self.settingsBrowser = SettingsWindow(self)
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
        self.do_run.connect(self.processImages)
        self.do_update.connect(self.populateComboBox)
        self.do_update.connect(self.setupLabels)


        self.clearButton.clicked.connect(self.clear)
        self.exportButton.clicked.connect(lambda i: self.show_report.emit(self.currentIndex))

        #self.make_report.connect(self.dialogTextBrowser.printerSetup)
        self.show_report.connect(self.do_show_report)
        self.make_report.connect(self.dialogTextBrowser.do_test)

        #sends export data sets
        self.sendProcessedImagesList.connect(self.dialogTextBrowser.receiver)

        self.settingsButton.clicked.connect(self.settingsBrowser.do_change)
        self.settingsBrowser.sendValues.connect(self.updateValues)

        # sends off a signal containing string.
        # Conveniently the string will be the name of the file.
        self.selectImgBox.activated[str].connect(self.changeState)

        """This is to gain better insight into Slots and Signals.
        def userLog(int):
            print("User requested reported for image: {}".format(int))
        self.show_report.connect(userLog)
        """
    @pyqtSlot(float, float, float, float)
    def updateValues(self, uCut, lCut, angleInc, radStep):
        self.uCut = uCut
        self.lCut = lCut
        self.angleInc = angleInc
        self.radStep = radStep
        print(self.uCut, self.lCut, self.angleInc, self.radStep)

    def do_show_report(self):
        if (self.isStarted):
            self.make_report.emit(self.imgList[self.currentIndex], self.imgList)

    """
    Clears out canvas.
    """

    def clear(self):
        if (self.isStarted):
            self.kLabel.setText("k = ")
            self.muLabel.setText("mu =  ")
            # clears canvas
            self.cleanCanvas()
            self.filenames.clear()
            # clears combo-box
            self.selectImgBox.clear()
            # resets isStarted
            self.isStarted = False
            # empties all images
            self.imgList.clear()
            # resets current index
            self.currentIndex = 0

    """
    Allows user to select image to use.
    """

    def launch(self):
        self.filenames = []
        dialog = QFileDialog()
        filenames = dialog.getOpenFileNames(self, '', None)  # creates a list of fileNames
        for name in filenames[0]:
            self.filenames.append(pathlib.Path(name))
        self.do_run.emit()
        self.do_update.emit(self.currentIndex)
        self.removeTemp()

    """
    Processes selected images. Displays it onto a canvas.
    Technical: Creates img_model objects that encapsulate all of the useful data.
    """
    @pyqtSlot()
    def processImages(self):
        processedImagesList = []
        for filename in self.filenames:
            # Retrieve Figures from data analysis code
            k, th, R2, angDist, cartDist, logScl, orgImg = computerVision_BP.process_image(filename, self.uCut, self.lCut, self.angleInc, self.radStep)
            # Starting from Python3, there is a distinctin between bytes and str. Thus, I can't use
            # methods of str on bytes. However I need to do that in order to properly encode the image
            # into b64. The main thing is that bytes-way produces some improper characters that mess up
            # the decoding process. Hence, decode(utf-8) translates bytes into str.
            angDistEncoded = base64.encodebytes(open('angDist.png', 'rb').read()).decode('utf-8')
            cartDistEncoded = base64.encodebytes(open('cartDist.png', 'rb').read()).decode('utf-8')
            logSclEncoded = base64.encodebytes(open('logScl.png', 'rb').read()).decode('utf-8')
            orgImgEncoded = base64.encodebytes(open('orgImg.png', 'rb').read()).decode('utf-8')

            # Creates an object
            processedImage = img_model.ImgModel(
                filename=filename,
                k=k,
                th=th,
                R2 = R2,
                orgImg=orgImg,
                orgImgEncoded=orgImgEncoded,
                logScl=logScl,
                logSclEncoded=logSclEncoded,
                angDist=angDist,
                angDistEncoded=angDistEncoded,
                cartDist=cartDist,
                cartDistEncoded=cartDistEncoded,
                timeStamp=datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"))

            processedImagesList.append(processedImage)
            # Ordered Set
            if processedImage in self.imgList:
                self.imgList.remove(processedImage)
                self.imgList.add(processedImage)
            else:
                self.imgList.add(processedImage)
        self.sendProcessedImagesList.emit(processedImagesList, self.dataList, self.uCut, self.lCut, self.radStep, self.angleInc)
        processedImagesList = []
        if self.isStarted:
            # removes/deletes all canvases
            self.cleanCanvas()
        # fills canvas
        # TODO: send as signal!
        # example:
        #     self.updateCanvasSignal.emit(self.currentIndex)
        self.fillCanvas(self.imgList.__getitem__(self.currentIndex))
        # started
        self.isStarted = True

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
        self.imgCanvas = FigureCanvas(img.orgImg)
        self.logSclCanvas = FigureCanvas(img.logScl)
        self.angDistCanvas = FigureCanvas(img.angDist)
        self.cartDistCanvas = FigureCanvas(img.cartDist)
        # adds them to layout
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
        # Processes selected images; sets up the labels and fills selectImgBox with references to images.
        # TODO: Make an exception to catch IndexError, and pop the window with appropriate message.
        self.kLabel.setText("k = ")
        self.muLabel.setText("mu =  ")
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
        self.do_update.emit(self.currentIndex)
        self.removeTemp()

    """
    Removes files in temp directory. Prevents memory leak.
    """
    def removeTemp(self):
        #fix bug so that it does remove images only when they are selected.
        files = []
        files.append('angDist.png')
        files.append('orgImg.png')
        files.append('cartDist.png')
        files.append('logScl.png')
        for filename in files:
            os.remove(filename)

    """
    Sets up appropriate labels depending on which image is selected.
    """
    @pyqtSlot(int)
    def setupLabels(self, num):
        self.kLabel.setText("k = " + str(round(self.imgList.__getitem__(num).k, 2)))
        self.muLabel.setText("μ = " + str(round(self.imgList.__getitem__(num).th, 2)))
        self.RLabel.setText("R^2 = " + str(round(self.imgList.__getitem__(num).R2, 2)))

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
                self.kLabel.setText("k = " + str(round(image.k, 2)))
                self.muLabel.setText("mu = " + str(round(image.th, 2)))
                # sets current index to the index of the found image.
                self.currentIndex = self.imgList.index(image)


def main():
    """
    Enters an event-loop.
    """
    app = QtWidgets.QApplication(sys.argv)
    fft_app = fft_mainWindow()
    fft_app.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
