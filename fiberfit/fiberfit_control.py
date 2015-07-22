#!/usr/local/bin/python3

"""This is a control part of the GUI application"""
import os
import pathlib
import glob
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
from PyQt5.QtCore import QFileInfo  # In order to get a pathname to a file.
from fiberfit import img_model
from orderedset import OrderedSet
import base64
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QTextDocument
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt5.QtWidgets import QPushButton, QDialogButtonBox, QVBoxLayout, QDialog


class MyDialog(QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.textBrowser = QWebView(self)
        self.textBrowser.setHtml("This is a QTextBrowser!")

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addWidget(self.textBrowser)
        self.verticalLayout.addWidget(self.buttonBox)


    def createHtml(self, model):
        html = """
        <html> <link type="text/css" rel="stylesheet" href="ntm_style.css"> <body>
        <p> Image Name: {name} </p> <p> mu: %s </p>
        <p>k: {k} </p>
        <table>
            <tr>
                <td> <img src = \"orgImg.png\"/> </td>
                <td> <img src =\"logScl.png\"/> </td>
            </tr>
        </table>

        """.format(name = model.filename.stem, k = model.k)
        html += ("<html> <link type = \"text/css\" rel = \"stylesheet\" href = \"ntm_style.css\"> <body>")
        html += ("<p> Image Name: %s </p> <p> mu: %s </p> <p>k: %s </p> <table> <tr> <td> <img src = \"orgImg.png\"/> </td> <td> <img src =\"logScl.png\"/> </td> </tr> </table>" %
                 (model.filename.stem, model.th, model.k ))
        html += ("</body> </html>")
        print(html)
        return html

    @pyqtSlot(img_model.ImgModel)
    def do_test(self, model):
        print("Test?")
        self.textBrowser.setHtml(self.createHtml(model))
        self.show()

class fft_mainWindow(fiberfit_GUI.Ui_MainWindow, QtWidgets.QMainWindow):
    results = open('test.csv', 'a')  # All instances would have this as a starter. Initialized later in code.
    show_report = pyqtSignal(int)
    make_report = pyqtSignal(img_model.ImgModel)

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
        # All the events happen below
        self.startButton.clicked.connect(self.start)
        self.nextButton.clicked.connect(self.nextImage)
        self.prevButton.clicked.connect(self.prevImage)
        self.loadButton.clicked.connect(self.launch)
        self.clearButton.clicked.connect(self.clear)
        self.exportButton.clicked.connect(self.export)
        # sends off a signal containing string.
        # Conveniently the string will be the name of the file.
        self.selectImgBox.activated[str].connect(self.changeState)

        #New button
        self.pushButtonWindow = QPushButton(self)
        self.pushButtonWindow.setText("Click Me!")
        self.pushButtonWindow.clicked.connect(lambda i: self.show_report.emit(self.currentIndex))

        self.gridLayout.addWidget(self.pushButtonWindow)

        def userLog(int):
            print("User requested reported for image: {}".format(int))

        self.show_report.connect(userLog)

        #self.layout = QtGui.QHBoxLayout(self)
        #self.layout.addWidget(self.pushButtonWindow)
        self.dialogTextBrowser = MyDialog(self)

        def do_show_report(index):
            print('Shows report')
            self.make_report.emit(self.imgList[self.currentIndex])
            #self.dialogTextB3rowser.show()

        self.show_report.connect(do_show_report)
        self.make_report.connect(self.dialogTextBrowser.do_test)

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
    # @PyQt.Slot(List)
    def processImages(self):
        for filename in self.filenames:
            # Retrieve Figures from data analysis code
            k, th, angDist, cartDist, logScl, orgImg = computerVision_BP.process_image(filename)
            angDistEncoded = base64.encodestring(open('angDist.png', 'rb').read())
            cartDistEncoded = base64.encodestring(open('cartDist.png', 'rb').read())
            logSclEncoded = base64.encodestring(open('logScl.png', 'rb').read())
            orgImgEncoded = base64.encodestring(open('orgImg.png', 'rb').read())

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
            self.decodeFigures(1)
            self.printOutput(1)
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

    def printOutput(self, i):
        html = ""
        html += ("<html> <link type = \"text/css\" rel = \"stylesheet\" href = \"ntm_style.css\"> <body>")
        html += ("<p> Image Name: %s </p> <p> mu: %s </p> <p>k: %s </p> <table> <tr> <td> <img src = \"orgImg.png\"/> </td> <td> <img src =\"logScl.png\"/> </td> </tr> </table>" % (self.imgList.__getitem__(i).filename.stem, self.imgList.__getitem__(i).th, self.imgList.__getitem__(i).k ))
        html += ("</body> </html>")

    def printerSetup(self):
        printer = QPrinter()
        printer.setPageSize(QPrinter.Letter)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName('ResultTable.pdf')
        document = QTextDocument()
        document.setHtml(html)
        document.print_(printer)

    def changeState(self, filename):
        # find img
        for image in self.imgList:
            if image.filename.stem == filename:
                self.processImagesFromComboBox(image)
                self.kLabel.setText("k = " + str(round(image.k, 2)))
                self.muLabel.setText("mu = " + str(round(image.th, 2)))
                # sets current index to the index of the found image.
                self.currentIndex = self.imgList.index(image)

    def decodeFigures(self, i):
        orgImgDecoded = open("orgImg.png", "wb")
        orgImgDecoded.write(base64.b64decode(self.imgList.__getitem__(i).orgImgEncoded))
        orgImgDecoded.close()
        logSclDecoded = open("logScl.png", "wb")
        logSclDecoded.write(base64.b64decode(self.imgList.__getitem__(i).logSclEncoded))
        logSclDecoded.close()
        cartDistDecoded = open("cartDist.png", "wb")
        cartDistDecoded.write(base64.b64decode(self.imgList.__getitem__(i).cartDistEncoded))
        cartDistDecoded.close()
        angDistDecoded = open("angDist.png", "wb")
        angDistDecoded.write(base64.b64decode(self.imgList.__getitem__(i).angDistEncoded))


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