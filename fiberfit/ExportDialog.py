from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1000, 1200)
        Dialog.setMinimumSize(QtCore.QSize(570, 870))
        Dialog.setMaximumSize(QtCore.QSize(570, 870))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.webView = QtWebKitWidgets.QWebView(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.webView.sizePolicy().hasHeightForWidth())
        self.webView.setSizePolicy(sizePolicy)
        self.webView.setUrl(QtCore.QUrl("about:blank"))
        self.webView.setObjectName("webView")
        self.gridLayout.addWidget(self.webView, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.prevBut = QtWidgets.QPushButton(Dialog)
        self.prevBut.setObjectName("prevBut")
        self.horizontalLayout.addWidget(self.prevBut)
        self.nextBut = QtWidgets.QPushButton(Dialog)
        self.nextBut.setObjectName("nextBut")
        self.horizontalLayout.addWidget(self.nextBut)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.saveBox = QtWidgets.QDialogButtonBox(Dialog)
        self.saveBox.setStandardButtons(QtWidgets.QDialogButtonBox.SaveAll|QtWidgets.QDialogButtonBox.Save)
        self.saveBox.setObjectName("saveBox")
        self.horizontalLayout.addWidget(self.saveBox)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.prevBut.setText(_translate("Dialog", "<---"))
        self.nextBut.setText(_translate("Dialog", "--->"))

from PyQt5 import QtWebKitWidgets
