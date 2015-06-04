#!/usr/local/bin/python3

"""This is a control part of the GUI application"""

import sys
from fiberfit import fiberfit_GUI
from fiberfit import computerVision_BP
from fiberfit import fiberfit_pop
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap

class fft_mainWindow(fiberfit_GUI.Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self, Parent = None):
        super(fft_mainWindow, self).__init__()
        self.setupUi(self)
        self.startButton.clicked.connect(self.start)

    def start(self):
        computerVision_BP.main()
        pop = fiberfit_pop()
        map = QPixmap
        map.fromImage(computerVision_BP.figimage, Qt_ImageConversionFlags_flags=None)




app = QtWidgets.QApplication(sys.argv)
fft_app = fft_mainWindow()
fft_app.show()
sys.exit(app.exec_())


