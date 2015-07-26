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
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt5.QtWidgets import QDialogButtonBox, QVBoxLayout, QDialog
from fiberfit import SettingsDialog

class SettingsWindow(QDialog, SettingsDialog.Ui_Dialog):
    sendValues = pyqtSignal(float, float, float, float)
    def __init__(self, parent = None):
        super(SettingsWindow, self).__init__(parent)
        self.setupUi(self)
        self.sendValues.connect(fft_mainWindow.processImages)
        self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.acceptValues)

    @pyqtSlot()
    def makeChanges(self):
        self.show()

    def acceptValues(self):
        uCut = float(self.ttopField.text())
        lCut = float(self.tbottomField.text())
        angleInc = float(self.btopField.text())
        radStep = float(self.bbottomField.text())
        print(uCut, lCut, angleInc, radStep)
        self.sendValues.emit(uCut, lCut, angleInc, radStep)

class ReportDialog(QDialog):
    printerRequest = pyqtSignal()
    def __init__(self, parent=None):
        super(ReportDialog, self).__init__(parent)
        self.printer = QPrinter(QPrinter.PrinterResolution)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.textBrowser = QWebView(self)
        self.textBrowser.setHtml("This is a QTextBrowser!")
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addWidget(self.textBrowser)
        self.verticalLayout.addWidget(self.buttonBox)
        #Signals and slots:
        self.buttonBox.button(QDialogButtonBox.Save).clicked.connect(self.print)
        self.printerRequest.connect(self.printerSetup)

    def print(self):
        self.printerRequest.emit()
        self.textBrowser.print(self.printer)

    @pyqtSlot()
    def printerSetup(self):
        self.printer.setPageSize(QPrinter.A4)
        self.printer.setOutputFormat(QPrinter.PdfFormat)
        #self.printer.setPageMargins(10, 10 , 10 , 10 , QPrinter.Inch)
        self.printer.setFullPage(True)
        self.printer.setOutputFileName('ResultTable')


    def createHtml(self, model):
        html = """
        <html>
            <head>
                <link type="text/css" rel="stylesheet" href="ntm_style.css"/>
            </head>
            <body>
                <p> Image Name: {name} </p> <p> mu: {th} </p>
                <p>k: {k} </p>
                <table>
                    <tr>
                        <td> <img src = "data:image/png;base64,{encodedOrgImg}"/></td>
                        <td> <img src ="data:image/png;base64,{encodedLogScl}"/></td>
                    </tr>
                    <tr>
                        <td> <img src = "data:image/png;base64,{encodedAngDist}"/></td>
                        <td> <img src = "data:image/png;base64,{encodedCartDist}"/></td>
                    </tr>
                </table>
                <div class="footer">
                    {date}
                </div>
            </body>
        </html>
        """.format(name = model.filename.stem,th = model.th, k = model.k,
                   encodedOrgImg = model.orgImgEncoded.translate('bn\''),
                   encodedLogScl = model.logSclEncoded.translate('bn\''),
                   encodedAngDist = model.angDistEncoded.translate('bn\''),
                   encodedCartDist = model.cartDistEncoded.translate('bn\''),
                   date = model.timeStamp)
        #print(html)
        return html

    @pyqtSlot(img_model.ImgModel)
    def do_test(self, model):
        self.textBrowser.setHtml(self.createHtml(model))
        self.show()

class fft_mainWindow(fiberfit_GUI.Ui_MainWindow, QtWidgets.QMainWindow):
    results = open('test.csv', 'a')  # All instances would have this as a starter. Initialized later in code.
    show_report = pyqtSignal(int)
    make_report = pyqtSignal(img_model.ImgModel)
    change_settings = pyqtSignal()
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
        #Canvases to display the figures.
        self.imgCanvas = None
        self.logSclCanvas = None
        self.angDistCanvas = None
        self.cartDistCanvas = None
        #Pops up a dialog with
        self.dialogTextBrowser = ReportDialog(self)
        self.settingsBrowser = SettingsWindow(self)
        # All the events happen below
        self.startButton.clicked.connect(self.start)
        self.nextButton.clicked.connect(self.nextImage)
        self.prevButton.clicked.connect(self.prevImage)
        self.loadButton.clicked.connect(self.launch)
        self.clearButton.clicked.connect(self.clear)
        self.exportButton.clicked.connect(lambda i: self.show_report.emit(self.currentIndex))
        self.show_report.connect(self.do_show_report)
        self.make_report.connect(self.dialogTextBrowser.do_test)
        self.settingsButton.clicked.connect(self.do_change_settings)
        self.change_settings.connect(self.settingsBrowser.makeChanges)

        # sends off a signal containing string.
        # Conveniently the string will be the name of the file.
        self.selectImgBox.activated[str].connect(self.changeState)

        """This is to gain better insight into Slots and Signals.
        def userLog(int):
            print("User requested reported for image: {}".format(int))
        self.show_report.connect(userLog)
        """

    def do_change_settings(self):
        self.change_settings.emit()

    def do_show_report(self, index):
        print('Shows report')
        self.make_report.emit(self.imgList[self.currentIndex])

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
        dialog = QFileDialog()
        filenames = dialog.getOpenFileNames(self, '', None)  # creates a list of fileNames
        for name in filenames[0]:
            self.filenames.append(pathlib.Path(name))

    """
    Processes selected images. Displays it onto a canvas.
    Technical: Creates img_model objects that encapsulate all of the useful data.
    """
    @pyqtSlot(float, float, float, float)
    def processImages(self, uCut = float, lCut = float, angleInc = float, radialStep = float):
        if uCut == None:
            uCut = 2
        if lCut == None:
            lCut = 32
        if angleInc == None:
            angleInc = 1
        if radialStep == None:
            radialStep = 0.5
        for filename in self.filenames:
            # Retrieve Figures from data analysis code
            print(uCut, lCut, radialStep, angleInc)
            k, th, angDist, cartDist, logScl, orgImg = computerVision_BP.process_image(filename, uCut, lCut, radialStep, angleInc)
            # Starting from Python3, there is a distinctin between bytes and str. Thus, I can't use
            # methods of str on bytes. However I need to do that in order to properly encode the image
            # into b64. The main thing is that bytes-way produces some improper characters that mess up
            # the decoding process. Hence, decode(utf-8) translates bytes into str.
            angDistEncoded = base64.encodebytes(open('angDist.png', 'rb').read()).decode('utf-8')
            cartDistEncoded = base64.encodebytes(open('cartDist.png', 'rb').read()).decode('utf-8')
            logSclEncoded = base64.encodebytes(open('logScl.png', 'rb').read()).decode('utf-8')
            orgImgEncoded = base64.encodebytes(open('orgImg.png', 'rb').read()).decode('utf-8')

            #Creates an object
            processedImage = img_model.ImgModel(
                filename=filename,
                k=k,
                th=th,
                orgImg=orgImg,
                orgImgEncoded = orgImgEncoded,
                logScl=logScl,
                logSclEncoded = logSclEncoded,
                angDist=angDist,
                angDistEncoded = angDistEncoded,
                cartDist=cartDist,
                cartDistEncoded = cartDistEncoded,
                timeStamp=datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"))

            # Ordered Set
            self.imgList.add(processedImage)
            #TODO: Don't compute the ones that are already in.
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

    def populateComboBox(self):
        self.selectImgBox.clear()
        for element in self.imgList:
            self.selectImgBox.addItem(element.filename.stem)
        self.selectImgBox.setCurrentIndex(self.currentIndex)

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
        #TODO: Make an exception to catch IndexError, and pop the window with appropriate message.
        self.processImages()
        self.setupLabels(self.currentIndex)
        self.populateComboBox()

    """
    Sets up appropriate labels depending on which image is selected.
    """

    def setupLabels(self, num):
        self.kLabel.setText("k = " + str(round(self.imgList.__getitem__(num).k, 2)))
        self.muLabel.setText("mu = " + str(round(self.imgList.__getitem__(num).th, 2)))

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
    Exports results into a .csv file.
    """
    # TODO: Need to add saving of PDF option.
    def export(self):
        for i in range(self.csvIndex, len(self.imgList)):
            self.dataList.append(
                [self.imgList.__getitem__(i).filename.stem, self.imgList.__getitem__(i).th, self.imgList.__getitem__(i).k,
                 self.imgList.__getitem__(i).timeStamp])
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