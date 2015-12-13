#!/usr/local/bin/python3

"""This is a control part of the GUI application"""
import pathlib
import sys
import csv
import datetime
import matplotlib
from PyQt5 import QtWebKitWidgets
import threading
import time
from PyPDF2 import PdfFileMerger as merger

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
from fiberfit import ErrorDialog
from PyQt5.QtGui import QTextDocument
import os
from PyQt5.QtWidgets import QDesktopWidget
from fiberfit import export_window


class ErrorDialog(QDialog, ErrorDialog.Ui_ErrorDialog):
    def __init__(self, parent=None, screenDim = None):
        super(ErrorDialog, self).__init__(parent)
        self.setupUi(self, screenDim)

    def show(self):
        self.exec_()

class SettingsWindow(QDialog, SettingsDialog.Ui_Dialog):
    genUCut = 2.0
    genLCut = 32.0
    genAngInc = 1.0
    genRadStep = 0.5
    sendValues = pyqtSignal(float, float, float, float)

    def __init__(self, parent=None, screenDim = None):
        super(SettingsWindow, self).__init__(parent)
        self.setupUi(self, screenDim)
        self.valuesStack = [(self.genUCut, self.genLCut, self.genAngInc, self.genRadStep)]
        self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.make_change)
        self.buttonBox.button(QDialogButtonBox.Reset).clicked.connect(self.reset_changes)
        self.setupDefaultValues()
        self.rejected.connect(self.reset_changes)

    """
    Resets changes to the last saved changes.
    """

    def reset_changes(self):
        self.ttopField.setText(self.valuesStack[self.valuesStack.__len__() - 1][0].__str__())
        self.tbottomField.setText(self.valuesStack[self.valuesStack.__len__() - 1][1].__str__())
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
        self.exec_()

class ReportDialog(QDialog, export_window.Ui_Dialog):
    """ Summary of ReportDialog.

    Represents a pop-up dialog when user presses "Export" button. Dialog contains a preview of the report containing
    values of "mu", "k", "R^2" and the replica of FiberFit main window's when a sample has been processed.

    Attributes:
        - do_print is a signal sent when either Save or Save All button are pressed.
        - do_excel is a signal starting the process of exporting results into an .csv format
        - sendDataList is a signal that sends a list containing already exported images back to FiberFit.
        - dataList is a list representing already exported images
        - screenDim stores a screen dimension
        - document is an instance of QTextDocument that
        TODO: List the other attributes.
    """
    do_print = pyqtSignal()
    do_excel = pyqtSignal()
    sendDataList = pyqtSignal(list)

    def __init__(self, parent=None, screenDim=None):

        super(ReportDialog, self).__init__(parent)
        self.dataList = []
        self.setupUi(self)
        self.screenDim = screenDim
        self.document = QTextDocument()
        #list that keeps track of only selected images
        self.list = []
        #list that contains all of the stored images
        self.wholeList = OrderedSet()
        self.savedfiles = None
        self.currentModel = None
        # settings
        self.uCut = 0
        self.lCut = 0
        self.angleInc = 0
        self.radStep = 0
        #  states
        """
        0 -> single
        1 -> multiple
        2 -> append
        """
        self.isReport = True
        self.isSummary = False
        self.reportOption = 2
        self.merger = merger()
        # printer
        self.printer = QPrinter(QPrinter.PrinterResolution)
        # Signals and slots:
        self.do_excel.connect(self.exportExcel)
        self.webView = QtWebKitWidgets.QWebView()

        # self.checkBox_report.stateChanged.connect(self.topLogicHandler)
        self.checkBox_summary.stateChanged.connect(self.topLogicHandler)

        self.radio_multiple.toggled.connect(self.toggleHandler)
        self.radio_single.toggled.connect(self.toggleHandler)
        self.radio_append.toggled.connect(self.toggleHandler)

        self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.exportHandler)
       # self.saveBox.button(QDialogButtonBox.SaveAll).clicked.connect(self.saveas)
       # self.saveBox.button(QDialogButtonBox.Save).clicked.connect(self.saveas)
        self.do_print.connect(self.print)
        self.rejected.connect(self.resetOptions)

    def resetOptions(self):
        #self.checkBox_report.setChecked(False)
        self.checkBox_summary.setChecked(False)
        #self.radio_none.setChecked(True)
        #self.radio_none.setEnabled(False)
        self.radio_append.setChecked(True)
        self.radio_multiple.setChecked(False)
        self.radio_single.setChecked(False)
        #self.radio_single.setEnabled(False)
        #self.radio_multiple.setEnabled(False)
        #self.radio_append.setEnabled(False)

    def exportHandler(self):
        if self.isSummary and self.isReport is False:
            self.saveas()
        elif (self.reportOption == 0 or self.reportOption == 2 or self.reportOption == 1) and self.isSummary is False:
            self.saveas()
        elif self.isSummary and self.isReport:
            self.saveas()

    def toggleHandler(self):
        if self.radio_single.isChecked():
            self.reportOption = 0
            self.isReport = True
        elif self.radio_multiple.isChecked():
            self.reportOption = 1
            self.isReport = True
        elif self.radio_append.isChecked():
            self.reportOption = 2
            self.isReport = True
        elif self.radio_none.isChecked():
            self.reportOption = -1
            self.isReport = False

       #  print("Status: " + str(self.reportOption))

    def topLogicHandler(self):
        if self.checkBox_summary.isChecked():
            self.isSummary = True
        elif self.checkBox_summary.isChecked() is False:
            self.isSummary = False

    """Makes excel spreadsheet.
    """
    # TODO: Need to work here!
    @pyqtSlot()
    def exportExcel(self):
        if self.dataList.__len__() == 0:
            self.dataList.append(
                [self.wholeList[0].filename.stem,
                 self.uCut,
                 self.lCut,
                 self.radStep,
                 self.angleInc,
                 self.wholeList[0].th,
                 self.wholeList[0].k,
                 self.wholeList[0].R2,
                 self.wholeList[0].timeStamp])
        # temp = self.list
        temp = []
        for i in range(0, self.wholeList.__len__()):
            temp.append(self.wholeList[i])
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
                                             round(temp[j].th, 2),
                                             round(temp[j].k, 2),
                                             round(temp[j].R2, 2),
                                             temp[j].timeStamp])
                    temp.remove(temp[j])
                    found = True
        for k in range(0, len(temp)):
            self.dataList.append([temp[k].filename.stem,
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
            a.writerow(['Name', 'LowerCut', 'UpperCut', 'RadialStep', 'AngleIncrement', 'Mu', 'K', 'R^2', 'Time'])
            a.writerows(self.dataList)
        fft_mainWindow.dataList = self.dataList

    """
    Pops out a dialog allowing user to select where to save the image.
    """
    def saveas(self):
        dialog = QFileDialog()
        if (self.reportOption == 0):
            self.savedfiles = pathlib.Path(dialog.getSaveFileName(self, "Export", self.currentModel.filename.stem)[0])
            #  print(self.savedfiles)
            self.close()

        elif (self.reportOption == 1):
            self.savedfiles = pathlib.Path(dialog.getSaveFileName(self, "Export",
                                                                  "Image Name")[
                                               0])
            self.close()
        elif (self.reportOption == 2):
            self.savedfiles = pathlib.Path(dialog.getSaveFileName(self, "Export",
                                                                  "Report")[
                                               0])
            # print(self.savedfiles)
            self.close()
        if (self.isSummary and not self.isReport):
            self.savedfiles = pathlib.Path(dialog.getSaveFileName(self, "Export",
                                                                  "SummaryTable")[
                                               0])
        # print("Did I make it here?")
        # print(str(self.isReport))
        self.printerSetup()
        if (self.isReport == True):
            self.do_print.emit()
        #    print("EMITTED!")
        if self.isSummary == True:
            self.do_excel.emit()


    """
    Checks which button sent a signal. Based on that it either prints all images or just a single specific image.
    """

    def print(self):
        if (self.reportOption == 1):
            for model in self.wholeList:
                self.document.setHtml(self.createHtml(model, forPrinting=True))
                self.printer.setOutputFileName(
                    self.savedfiles.parents[0].__str__() + '/' + self.savedfiles.name.replace("Image Name", "") + model.filename.stem + '.pdf')
                self.document.print(self.printer)
        elif (self.reportOption == 0):
            self.document.print(self.printer)

        elif (self.reportOption == 2):
            self.merger = merger()
            for model in self.wholeList:
                self.document.setHtml(self.createHtml(model, forPrinting=True))
                name = self.savedfiles.__str__() + '.pdf'
                print(name)
                self.printer.setOutputFileName(
                    self.savedfiles.parents[0].__str__() + '/' + self.savedfiles.name.replace("Image Name", "") + model.filename.stem + '.pdf')
                self.document.print(self.printer)
                input = open(self.savedfiles.parents[0].__str__() + '/' + self.savedfiles.name.replace("Image Name", "") + model.filename.stem + '.pdf', "rb")
                self.merger.append(input)
                os.remove(self.savedfiles.parents[0].__str__() + '/' + self.savedfiles.name.replace("Image Name", "") + model.filename.stem + '.pdf')

            out = open(name, "wb")
            self.merger.write(out)
            self.merger.close()
    """
    Sets up default instructions for printer.
    """

    def printerSetup(self):
        self.printer.setPageSize(QPrinter.A4)
        self.printer.setOutputFormat(QPrinter.PdfFormat)
        self.printer.setFullPage(True)
        self.printer.setOutputFileName(str(self.savedfiles)+".pdf")

    """
    Creates html-based report that shows the basic information about the sample.
    """

    def createHtml(self, model, forPrinting):
        # for printing
        if forPrinting:
            html = """
        <html>
            <head>
                <link type="text/css" rel="stylesheet" href="ntm_style.css"/>
            </head>
            <body>
                <p> Image Name: {name} </p> <p> μ: {th} </p>
                <p>k: {k} </p>
                <p>R^2: {R2} </p>
                <br>
                <table>
                    <tr>
                        <td> <img src = "data:image/png;base64,{encodedOrgImg}" width = "250", height = "250" /></td>
                        <td> <img src ="data:image/png;base64,{encodedLogScl}" width = "250", height = "250"/></td>
                    </tr>
                    <tr>
                        <td> <img src = "data:image/png;base64,{encodedAngDist}" width = "250", height = "250" /></td>
                        <td> <img src = "data:image/png;base64,{encodedCartDist}" width = "250", height = "250" /></td>
                    </tr>
                </table>
                <p><br><br><br><br><br>
                    {date}
                </p>
            </body>
        </html>
        """.format(name=model.filename.stem, th=round(model.th, 2), k=round(model.k, 2), R2=round(model.R2, 2),
                   encodedOrgImg=model.orgImgEncoded4.translate('bn\''),
                   encodedLogScl=model.logSclEncoded4.translate('bn\''),
                   encodedAngDist=model.angDistEncoded4.translate('bn\''),
                   encodedCartDist=model.cartDistEncoded4.translate('bn\''),
                   date=model.timeStamp)
            return html
        else:
           # for display
            html = """
            <html>
                <head>
                    <link type="text/css" rel="stylesheet" href="ntm_style.css"/>
                </head>
                <body>
                    <p> Image Name: {name} </p> <p> μ: {th} </p>
                    <p>k: {k} </p>
                    <p>R^2: {R2} </p>
                    <br>
                    <table>
                        <tr>
                            <td> <img src = "data:image/png;base64,{encodedOrgImg}" width = "{width}", height = "{heigth}" /></td>
                            <td> <img src ="data:image/png;base64,{encodedLogScl}" width = "{width}", height = "{heigth}"/></td>
                        </tr>
                        <tr>
                            <td> <img src = "data:image/png;base64,{encodedAngDist}" width = "{width}", height = "{heigth}" /></td>
                            <td> <img src = "data:image/png;base64,{encodedCartDist}" width = "{width}", height = "{heigth}" /></td>
                        </tr>
                    </table>
                    <p>
                        {date}
                    </p>
                </body>
            </html>
            """.format(name=model.filename.stem, th=round(model.th, 2), k=round(model.k, 2), R2=round(model.R2, 2),
                   encodedOrgImg=model.orgImgEncoded.translate('bn\''),
                   encodedLogScl=model.logSclEncoded.translate('bn\''),
                   encodedAngDist=model.angDistEncoded.translate('bn\''),
                   encodedCartDist=model.cartDistEncoded.translate('bn\''),
                   width = (0.1*self.screenDim.width()).__str__(),
                   heigth = (0.1*self.screenDim.width()).__str__(),
                   date=model.timeStamp)
            return html

    """
    Makes report for an image that was active when user pressed Export button.
    """

    @pyqtSlot(img_model.ImgModel)
    def do_test(self, model):
        self.webView.setHtml(self.createHtml(model, False))
        self.document.setHtml(self.createHtml(model, True))
        self.currentModel = model
        self.show()

    """
    Received an information from FiberFit applicatin with necessary report data.
    """

    @pyqtSlot(list, list, OrderedSet, float, float, float, float)
    def receiver(self, selectedImgs, dataList, imgList, uCut, lCut, radStep, angleInc):
        self.dataList = dataList
        self.list = selectedImgs
        self.wholeList = imgList
        self.uCut = uCut
        self.lCut = lCut
        self.radStep = radStep
        self.angleInc = angleInc

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
    sendProcessedImageCounter = pyqtSignal(int, img_model.ImgModel, list)

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
        # Canvases to display the figures.
        self.imgCanvas = None
        self.logSclCanvas = None
        self.angDistCanvas = None
        self.cartDistCanvas = None
        # Pops up a dialog with
        self.dialogTextBrowser = ReportDialog(self, self.screenDim)
        self.settingsBrowser = SettingsWindow(self, self.screenDim)
        self.errorBrowser = ErrorDialog(self, self.screenDim)
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

        """This is to gain better insight into Slots and Signals.
        def userLog(int):
            print("User requested reported for image: {}".format(int))
        self.show_report.connect(userLog)
        """

    """
    Updates the settings
    """
    @pyqtSlot(float, float, float, float)
    def updateValues(self, uCut, lCut, angleInc, radStep):
        self.uCut = uCut
        self.lCut = lCut
        self.angleInc = angleInc
        self.radStep = radStep


    def runner(self):
        pThread = myThread(self.sendProcessedImageCounter)
        pThread.update_values(self.uCut, self.lCut, self.angleInc, self.radStep, self.screenDim, self.dpi, self.filenames)
        self.progressBar.setValue(0)
        pThread.start()

    """
    Function that signals to show the report.
    """

    def do_show_report(self):
        if (self.isStarted):
            self.make_report.emit(self.imgList[self.currentIndex])

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
            # clears canvas
            self.cleanCanvas()
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

    """
    Allows user to select image to use.
    """

    def launch(self):
        self.filenames = []
        dialog = QFileDialog()
        filenames = dialog.getOpenFileNames(self, '', None)  # creates a list of fileNames
        for name in filenames[0]:
            self.filenames.append(pathlib.Path(name))
        self.progressBar.setMaximum(len(filenames[0]))
        self.do_run.emit()

    """
    Processes selected images. Displays it onto a canvas.
    Technical: Creates img_model objects that encapsulate all of the useful data.
    """

    @pyqtSlot(int, img_model.ImgModel, list)
    def processImages(self, count, processedImage, processedImagesList):
        # Ordered Set
        if processedImage in self.imgList:
            self.imgList.remove(processedImage)
            self.imgList.add(processedImage)
        else:
            self.imgList.add(processedImage)
        self.sendProcessedImagesList.emit(processedImagesList, self.dataList, self.imgList, self.uCut, self.lCut, self.radStep,
                                          self.angleInc)

        if self.isStarted:
            # removes/deletes all canvases
            self.cleanCanvas()
        # fills canvas
        self.fillCanvas(self.imgList.__getitem__(self.currentIndex))
        self.applyResizing()
        # started
        self.isStarted = True
        self.do_update.emit(self.currentIndex)
        self.removeTemp()
        #  Setting progress bar business
        self.progressBar.setValue(count)
        self.progressBar.valueChanged.emit(self.progressBar.value())

    """
    Makes so that screen can be resized after the images loaded.
    """

    def applyResizing(self):
        self.resize(0.3 * self.screenDim.width(), 0.7 *self.screenDim.height())
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
        self.muLabel.setText("μ =  ")
        self.RLabel.setText(('R' + u"\u00B2") + " = ")
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
                self.kLabel.setText("k = " + str(round(image.k, 2)))
                self.muLabel.setText("μ = " + str(round(image.th, 2)))
                self.RLabel.setText(('R' + u"\u00B2") + " = " + str(round(image.R2, 2)))
                # sets current index to the index of the found image.
                self.currentIndex = self.imgList.index(image)

class myThread(threading.Thread):

    def __init__(self, sig):
        super(myThread, self).__init__()
        self.uCut = 0
        self.lCut = 0
        self.angleInc = 0
        self.radStep = 0
        self.screenDim = 0
        self.dpi = 0
        self.sig = sig
        self.filenames = []

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
        for filename in self.filenames:
            # Retrieve Figures from data analysis code
            try:
                k, th, R2, angDist, angDist4, cartDist, cartDist4, logScl, logScl4, orgImg, orgImg4, figWidth, figHeigth = computerVision_BP.process_image(filename,
                                                                                               self.uCut,
                                                                                               self.lCut, self.angleInc,
                                                                                               self.radStep, self.screenDim,
                                                                                               self.dpi)

                # Starting from Python3, there is a distinctin between bytes and str. Thus, I can't use
                # methods of str on bytes. However I need to do that in order to properly encode the image
                # into b64. The main thing is that bytes-way produces some improper characters that mess up
                # the decoding process. Hence, decode(utf-8) translates bytes into str.

                angDistEncoded = base64.encodebytes(open('angDist.png', 'rb').read()).decode('utf-8')
                cartDistEncoded = base64.encodebytes(open('cartDist.png', 'rb').read()).decode('utf-8')
                logSclEncoded = base64.encodebytes(open('logScl.png', 'rb').read()).decode('utf-8')
                orgImgEncoded = base64.encodebytes(open('orgImg.png', 'rb').read()).decode('utf-8')

                angDistEncoded4 = base64.encodebytes(open('angDist4.png', 'rb').read()).decode('utf-8')
                cartDistEncoded4 = base64.encodebytes(open('cartDist4.png', 'rb').read()).decode('utf-8')
                logSclEncoded4 = base64.encodebytes(open('logScl4.png', 'rb').read()).decode('utf-8')
                orgImgEncoded4 = base64.encodebytes(open('orgImg4.png', 'rb').read()).decode('utf-8')

                # Creates an object
                processedImage = img_model.ImgModel(
                    filename=filename,
                    k=k,
                    th=th,
                    R2=R2,
                    orgImg=orgImg,
                    orgImgEncoded=orgImgEncoded,
                    orgImg4=orgImg4,
                    orgImgEncoded4 = orgImgEncoded4,
                    logScl=logScl,
                    logSclEncoded=logSclEncoded,
                    logScl4 = logScl4,
                    logSclEncoded4 = logSclEncoded4,
                    angDist=angDist,
                    angDistEncoded=angDistEncoded,
                    angDist4 = angDist4,
                    angDistEncoded4 = angDistEncoded4,
                    cartDist=cartDist,
                    cartDistEncoded=cartDistEncoded,
                    cartDist4 = cartDist4,
                    cartDistEncoded4 = cartDistEncoded4,
                    timeStamp= datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"))

                processedImagesList.append(processedImage)
                count += 1

            except TypeError:
                self.errorBrowser.show()
            except ValueError:
                self.errorBrowser.show()
            except OSError:
                self.errorBrowser.show()

            self.sig.emit(count, processedImage, processedImagesList)
            time.sleep(0.5)

def main():
    """
    Enters an event-loop.
    """
    app = QtWidgets.QApplication(sys.argv)
    fft_app = fft_mainWindow()
    fft_app.receiveDim()

    fft_app.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
