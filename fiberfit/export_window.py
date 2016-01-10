# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/azatulepbergenov/Desktop/export_window.ui'
#
# Created: Sat Nov 28 23:29:57 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog, screenDim):
        Dialog.setObjectName("Dialog")
        # Dialog.resize(421, 255)
        Dialog.resize(0.2 * screenDim.width(), 0.2 * screenDim.height())
        # Dialog.setMinimumSize(QtCore.QSize(0.12 * screenDim.width(), 0.12 * screenDim.height()))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.checkBox_summary = QtWidgets.QCheckBox(Dialog)
        self.checkBox_summary.setObjectName("checkBox_summary")
        self.horizontalLayout.addWidget(self.checkBox_summary)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 3)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 2, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.radio_none = QtWidgets.QRadioButton(Dialog)
        self.verticalLayout.addWidget(self.radio_none)
        #  self.radio_none.setChecked(True)
        self.radio_none.setEnabled(True)

        self.radio_single = QtWidgets.QRadioButton(Dialog)
        self.radio_single.setObjectName("radio_single")
        self.radio_single.setEnabled(True)
        self.verticalLayout.addWidget(self.radio_single)
        self.radio_multiple = QtWidgets.QRadioButton(Dialog)
        self.radio_multiple.setEnabled(True)
        self.radio_multiple.setObjectName("radio_multiple")
        self.verticalLayout.addWidget(self.radio_multiple)
        self.radio_append = QtWidgets.QRadioButton(Dialog)
        self.radio_append.setEnabled(True)
        self.radio_append.setChecked(True)
        self.radio_append.setObjectName("radio_append")
        self.verticalLayout.addWidget(self.radio_append)



        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 2, 2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Export Results"))
        self.label.setText(_translate("Dialog", "Report (PDF)"))
        self.checkBox_summary.setText(_translate("Dialog", "Summary Table (.xlsx)"))
        self.radio_single.setText(_translate("Dialog", "Single"))
        self.radio_multiple.setText(_translate("Dialog", "Multiple"))
        self.radio_append.setText(_translate("Dialog", "Multiple (Append)"))
        self.radio_none.setText(_translate("Dialog", "None"))

