from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    """
    Defines the view of the Settings dialog, which pops out when the Settings button was pressed.
    """
    def setupUi(self, Dialog, screenDim):
        """
        Sets up all of the GUI components of the Settings dialog.
        Created by PyQt5 UI code generator 5.4
        :param Dialog: instance of settings.SettingsWindow
        :param screenDim: dimensions of the screen
        :return: none

        """
        Dialog.setObjectName("Dialog")
        Dialog.resize(0.12 * screenDim.width(), 0.65 * screenDim.height())
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.topDescr = QtWidgets.QLabel(Dialog)
        self.topDescr.setWordWrap(True)
        self.topDescr.setContentsMargins(0, 0, 0, 0)
        self.topDescr.setObjectName("topDescr")
        self.verticalLayout_3.addWidget(self.topDescr)
        self.upperFrame = QtWidgets.QFrame(Dialog)
        self.upperFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.upperFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.upperFrame.setObjectName("upperFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.upperFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.upperLabel = QtWidgets.QLabel(self.upperFrame)
        self.upperLabel.setWordWrap(True)
        self.upperLabel.setContentsMargins(0, 0, 0, 0)
        self.upperLabel.setObjectName("upperLabel")
        self.horizontalLayout.addWidget(self.upperLabel)
        self.tfieldFrame = QtWidgets.QFrame(self.upperFrame)
        self.tfieldFrame.setMinimumSize(QtCore.QSize(70, 80))
        self.tfieldFrame.setMaximumSize(QtCore.QSize(70, 80))
        self.tfieldFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tfieldFrame.setObjectName("tfieldFrame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tfieldFrame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ttopField = QtWidgets.QLineEdit(self.tfieldFrame)
        self.ttopField.setMaximumSize(QtCore.QSize(50, 50))
        self.ttopField.setObjectName("ttopField")
        self.verticalLayout.addWidget(self.ttopField)
        self.tbottomField = QtWidgets.QLineEdit(self.tfieldFrame)
        self.tbottomField.setMaximumSize(QtCore.QSize(50, 50))
        self.tbottomField.setObjectName("tbottomField")
        self.verticalLayout.addWidget(self.tbottomField)
        self.horizontalLayout.addWidget(self.tfieldFrame)
        self.verticalLayout_3.addWidget(self.upperFrame)
        self.bottomDescr = QtWidgets.QLabel(Dialog)
        self.bottomDescr.setWordWrap(True)
        self.bottomDescr.setContentsMargins(0, 0, 0, 0)
        self.bottomDescr.setObjectName("bottomDescr")
        self.verticalLayout_3.addWidget(self.bottomDescr)
        self.bottomFrame = QtWidgets.QFrame(Dialog)
        self.bottomFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.bottomFrame.setObjectName("bottomFrame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.bottomFrame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.bottomLabel = QtWidgets.QLabel(self.bottomFrame)
        self.bottomLabel.setWordWrap(True)
        self.bottomLabel.setContentsMargins(0, 0, 0, 0)
        self.bottomLabel.setObjectName("bottomLabel")
        self.horizontalLayout_2.addWidget(self.bottomLabel)
        self.bfieldFrame = QtWidgets.QFrame(self.bottomFrame)
        self.bfieldFrame.setMinimumSize(QtCore.QSize(70, 80))
        self.bfieldFrame.setMaximumSize(QtCore.QSize(70, 80))
        self.bfieldFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.bfieldFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.bfieldFrame.setObjectName("bfieldFrame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.bfieldFrame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btopField = QtWidgets.QLineEdit(self.bfieldFrame)
        self.btopField.setMaximumSize(QtCore.QSize(50, 50))
        self.btopField.setObjectName("btopField")
        self.verticalLayout_2.addWidget(self.btopField)
        self.bbottomField = QtWidgets.QLineEdit(self.bfieldFrame)
        self.bbottomField.setMaximumSize(QtCore.QSize(50, 50))
        self.bbottomField.setObjectName("bbottomField")
        self.verticalLayout_2.addWidget(self.bbottomField)
        self.horizontalLayout_2.addWidget(self.bfieldFrame)
        self.verticalLayout_3.addWidget(self.bottomFrame)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Reset|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)
        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        """
        Sets up appropriate text values for the UI.
        :param Dialog: instance of settings.SettingsWindow
        :return: none

        """
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Settings", "Settings"))
        self.topDescr.setText(_translate("Dialog", "<b>Band-Pass Filter Settings</b>:\nInput fiber width -the frequency will be calculated using f = N/(2*t), where N is the image dimension. "))
        self.upperLabel.setText(_translate("Dialog", "Upper Cutoff (Smaller Thickness): \n"
"\n"
"Lower Cutoff (Larger Thickness): "))
        self.bottomDescr.setText(_translate("Dialog", "<b>Summation Increment Settings: \n</b>"
"\nInput the increment for angle summation (degrees) and the interpolation increment for radial summation (pixels)."))
        self.bottomLabel.setText(_translate("Dialog", "Angle Increment: \n"
"\n"
"Radial Step Size: "))