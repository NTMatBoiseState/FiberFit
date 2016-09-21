import sys
sys.path.append("/fiberfit/")
from src.fiberfit_gui import export_window
from src.fiberfit_control.support import img_model

from PyQt5.QtWidgets import QDialogButtonBox, QDialog, QFileDialog
from PyQt5.QtGui import QTextDocument
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyPDF2 import PdfFileMerger as merger
from PyQt5 import QtWebKitWidgets
import csv
from orderedset import OrderedSet
import pathlib
import os

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

    def __init__(self, fft_mainWindow,parent=None, screenDim=None):

        super(ReportDialog, self).__init__(parent)
        self.fft_mainWindow=fft_mainWindow
        self.dataList = []
        self.setupUi(self, screenDim)
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
        self.do_print.connect(self.print)
        self.rejected.connect(self.resetOptions)
        self.topLogicHandler()

    def resetOptions(self):
        self.checkBox_summary.setChecked(False)
        self.radio_append.setChecked(True)
        self.radio_multiple.setChecked(False)
        self.radio_single.setChecked(False)

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
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        elif self.radio_multiple.isChecked():
            self.reportOption = 1
            self.isReport = True
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        elif self.radio_append.isChecked():
            self.reportOption = 2
            self.isReport = True
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        elif self.radio_none.isChecked():
            self.reportOption = -1
            self.isReport = False
            if (not self.checkBox_summary.isChecked()):
                self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

    def topLogicHandler(self):
        if self.checkBox_summary.isChecked():
            self.isSummary = True
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        elif self.checkBox_summary.isChecked() is False:
            self.isSummary = False
            if (self.radio_none.isChecked()):
                self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

    @pyqtSlot()
    def exportExcel(self):
        if self.dataList.__len__() == 0:
            self.dataList.append(
                [self.wholeList[0].filename.stem,
                 self.uCut,
                 self.lCut,
                 self.radStep,
                 self.angleInc,
                 self.wholeList[0].sig,
                 self.wholeList[0].th,
                 self.wholeList[0].k,
                 self.wholeList[0].R2,
                 self.wholeList[0].timeStamp])
        temp = []
        for i in range(0, self.wholeList.__len__()):
            temp.append(self.wholeList[i])
        for i in range(0, len(self.dataList)):
            found = False
            for j in range(0, len(temp)):
                # One image from list is at most can equal to one another image from temp
                if found is False and self.dataList[i][0] == temp[j].filename.stem:
                    self.dataList.remove(self.dataList[i])
                    self.dataList.insert(i, [temp[j].filename.stem,
                                             self.uCut,
                                             self.lCut,
                                             self.radStep,
                                             self.angleInc,
                                             round(temp[j].sig[0], 2),
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
                                  round(temp[k].sig[0], 2),
                                  round(temp[k].th, 2),
                                  round(temp[k].k, 2),
                                  round(temp[k].R2, 2),
                                  temp[k].timeStamp])
        with open(str(self.savedfiles.parents[0]) + '/summary.csv', 'w') as csvfile:
            a = csv.writer(csvfile)
            a.writerow(['Name', 'LowerCut', 'UpperCut', 'RadialStep', 'AngleIncrement', 'Sig', 'Mu', 'K', 'R^2', 'Time'])
            a.writerows(self.dataList)
        self.fft_mainWindow.dataList = self.dataList

    def saveas(self):
        """
        Pops out a dialog allowing user to select where to save the image.
        """
        dialog = QFileDialog()
        if (self.reportOption == 0):
            self.savedfiles = pathlib.Path(dialog.getSaveFileName(self, "Export", self.currentModel.filename.stem)[0])
            self.close()
        elif (self.reportOption == 1):
            self.savedfiles = pathlib.Path(dialog.getSaveFileName(self, "Export",
                                                                  "Image Name")[0])
            self.close()
        elif (self.reportOption == 2):
            self.savedfiles = pathlib.Path(dialog.getSaveFileName(self, "Export",
                                                                  "Report")[0])
            self.close()
        if (self.isSummary and not self.isReport):
            self.savedfiles = pathlib.Path(dialog.getSaveFileName(self, "Export",
                                                                  "SummaryTable")[0])
        self.printerSetup()
        if (self.isReport == True):
            self.do_print.emit()
        if self.isSummary == True:
            self.do_excel.emit()

    def print(self):
        """
        Checks which button sent a signal. Based on that it either prints all images or just a single specific image.
        """
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

    def printerSetup(self):
        """
        Sets up default instructions for printer.
        """
        self.printer.setPageSize(QPrinter.Letter)
        self.printer.setOutputFormat(QPrinter.PdfFormat)
        self.printer.setFullPage(True)
        self.printer.setOutputFileName(str(self.savedfiles)+".pdf")

    def createHtml(self, model, forPrinting):
        """
        Creates html-based report that shows the basic information about the sample.
        """
        # for printing
        if forPrinting:
            html = """
        <html>
            <head>
                <link type="text/css" rel="stylesheet" href="ntm_style.css"/>
            </head>
            <body>
                <p> Image Name: {name} </p> <p> μ: {th}° </p>
                <p>k: {k} </p>
                <p>R^2: {R2} </p>
                <p>σ: {sig}°</p>
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
                <p><br><br>
                    {date}
                </p>
            </body>
        </html>
        """.format(name=model.filename.stem, th=round(model.th, 2), k=round(model.k, 2), R2=round(model.R2, 2),
                   sig = round(model.sig[0], 2),
                   encodedOrgImg=model.orgImgEncoded.translate('bn\''),
                   encodedLogScl=model.logSclEncoded.translate('bn\''),
                   encodedAngDist=model.angDistEncoded.translate('bn\''),
                   encodedCartDist=model.cartDistEncoded.translate('bn\''),
                   date=model.timeStamp)
            return html

    @pyqtSlot(img_model.ImgModel)
    def do_test(self, model):
        """
        Makes report for an image that was active when user pressed Export button.
        """
        self.webView.setHtml(self.createHtml(model, False))
        self.document.setHtml(self.createHtml(model, True))
        self.currentModel = model
        self.show()

    @pyqtSlot(list, list, OrderedSet, float, float, float, float)
    def receiver(self, selectedImgs, dataList, imgList, uCut, lCut, radStep, angleInc):
        """
        Received an information from FiberFit applicatin with necessary report data.
        """
        self.dataList = dataList
        self.list = selectedImgs
        self.wholeList = imgList
        self.uCut = uCut
        self.lCut = lCut
        self.radStep = radStep
        self.angleInc = angleInc

