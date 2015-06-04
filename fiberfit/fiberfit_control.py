#!/usr/local/bin/python3

"""This is a control part of the GUI application"""

import sys
from fiberfit import fiberfit_GUI
from fiberfit import computerVision_BP
from fiberfit import fiberfit_pop
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.Qt import*
class fft_mainWindow(fiberfit_GUI.Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self, Parent = None):
        super(fft_mainWindow, self).__init__()
        self.setupUi(self)
        self.startButton.clicked.connect(self.start)

    def start(self):
        computerVision_BP.main()

        #fiberfit_GUI.Ui_MainWindow(self).gridLayout.addWidget(matplot widget goes here)


        #pop = fiberfit_pop
        #map = QPixmap(computerVision_BP.figimage)
        #pop.Ui_StackedWidget.
        #pop.Ui_StackedWidget.setupUi(self)






app = QtWidgets.QApplication(sys.argv)
fft_app = fft_mainWindow()
fft_app.show()
sys.exit(app.exec_())


