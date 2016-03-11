#!usr/local/bin/python3

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ErrorDialog(object):
    def setupUi(self, ErrorDialog, screenDim):
        ErrorDialog.setObjectName("ErrorDialog")
        ErrorDialog.setEnabled(True)
        ErrorDialog.resize(0.15 * screenDim.width(), 0.15 * screenDim.height())
        ErrorDialog.setMinimumSize(QtCore.QSize(0.12 * screenDim.width(), 0.12 * screenDim.height()))
        ErrorDialog.setMaximumSize(QtCore.QSize(0.9 * screenDim.width(), 0.9 * screenDim.height()))
        self.gridLayout = QtWidgets.QGridLayout(ErrorDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(ErrorDialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 505, 156))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.label.setWordWrap(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(10000, 10000))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(14)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setFocusPolicy(QtCore.Qt.TabFocus)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setScaledContents(False)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_3)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(ErrorDialog)
        QtCore.QMetaObject.connectSlotsByName(ErrorDialog)

    def retranslateUi(self, ErrorDialog):
        _translate = QtCore.QCoreApplication.translate
        ErrorDialog.setWindowTitle(_translate("ErrorDialog", "Error"))
        self.label.setText(_translate("ErrorDialog",
"ERROR: Sorry, unfortunately, this image can not be processed. The specifications are as follow: an image must have 8-bit image depth, or, equivalently, gray color space and must be in .jpeg and .png formats."))