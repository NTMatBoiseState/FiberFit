# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/azatulepbergenov/Desktop/export_window.ui'
#
# Created: Sat Nov 28 23:07:51 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(413, 240)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.checkBox_report = QtWidgets.QCheckBox(Dialog)
        self.checkBox_report.setObjectName("checkBox_report")
        self.horizontalLayout.addWidget(self.checkBox_report)
        
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        
        self.checkBox_summary = QtWidgets.QCheckBox(Dialog)
        self.checkBox_summary.setObjectName("checkBox_summary")
        self.horizontalLayout.addWidget(self.checkBox_summary)
        
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.checkBox_single = QtWidgets.QCheckBox(Dialog)
        self.checkBox_single.setObjectName("checkBox_single")
        self.verticalLayout.addWidget(self.checkBox_single)
        self.checkBox_single.setEnabled(False)
        
        self.checkBox_multiple = QtWidgets.QCheckBox(Dialog)
        self.checkBox_multiple.setObjectName("checkBox_multiple")
        self.checkBox_multiple.setEnabled(False)
        
        self.verticalLayout.addWidget(self.checkBox_multiple)
        self.checkBox_append = QtWidgets.QCheckBox(Dialog)
        self.checkBox_append.setObjectName("checkBox_append")
        self.checkBox_append.setEnabled(False)
    
        self.verticalLayout.addWidget(self.checkBox_append)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 2, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.checkBox_report.setText(_translate("Dialog", "Report (PDF)"))
        self.checkBox_summary.setText(_translate("Dialog", "Summary Table (.xlsx)"))
        self.checkBox_single.setText(_translate("Dialog", "Single"))
        self.checkBox_multiple.setText(_translate("Dialog", "Multiple"))
        self.checkBox_append.setText(_translate("Dialog", "Multiple (Append)"))

