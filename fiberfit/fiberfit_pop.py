#!/usr/local/bin/python3

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_StackedWidget(object):
    def setupUi(self, StackedWidget):
        StackedWidget.setObjectName("StackedWidget")
        StackedWidget.resize(650, 580)
        self.fiberfit_pop = QtWidgets.QWidget()
        self.fiberfit_pop.setObjectName("fiberfit_pop")
        self.figure_frame = QtWidgets.QFrame(self.fiberfit_pop)
        self.figure_frame.setGeometry(QtCore.QRect(0, 0, 661, 541))
        self.figure_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.figure_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.figure_frame.setObjectName("figure_frame")
        self.mu_field = QtWidgets.QLineEdit(self.fiberfit_pop)
        self.mu_field.setGeometry(QtCore.QRect(130, 540, 100, 40))
        self.mu_field.setObjectName("mu_field")
        self.k_field = QtWidgets.QLineEdit(self.fiberfit_pop)
        self.k_field.setGeometry(QtCore.QRect(420, 540, 100, 40))
        self.k_field.setObjectName("k_field")
        StackedWidget.addWidget(self.fiberfit_pop)
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        StackedWidget.addWidget(self.page)

        self.retranslateUi(StackedWidget)
        StackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(StackedWidget)

    def retranslateUi(self, StackedWidget):
        _translate = QtCore.QCoreApplication.translate
        StackedWidget.setWindowTitle(_translate("StackedWidget", "StackedWidget"))
        self.mu_field.setText(_translate("StackedWidget", "mu ="))
        self.k_field.setText(_translate("StackedWidget", "k ="))

