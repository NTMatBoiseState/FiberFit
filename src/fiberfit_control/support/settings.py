from PyQt5.QtWidgets import QDialogButtonBox, QDialog
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from src.fiberfit_gui import settings_dialog as SettingsDialog


class SettingsWindow(QDialog, SettingsDialog.Ui_Dialog):
    """
    Class that contains the scientific parameter input to computerVision algorithm
    """
    # below are the default parameters for FiberFit
    genUCut = 2.0
    genLCut = 32.0
    genAngInc = 1.0
    genRadStep = 0.5
    sendValues = pyqtSignal(float, float, float, float)

    def __init__(self, parent=None, screenDim = None):
        super(SettingsWindow, self).__init__(parent)
        self.setupUi(self, screenDim)
        self.valuesStack = [(self.genUCut, self.genLCut, self.genAngInc, self.genRadStep)]
        self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.make_change)
        self.buttonBox.button(QDialogButtonBox.Reset).clicked.connect(self.reset_changes)
        self.setupDefaultValues()
        self.rejected.connect(self.reset_changes)

    def reset_changes(self):
        """
        Resets changes to the last saved changes.
        """
        self.ttopField.setText(self.valuesStack[self.valuesStack.__len__() - 1][0].__str__())
        self.tbottomField.setText(self.valuesStack[self.valuesStack.__len__() - 1][1].__str__())
        self.btopField.setText(self.valuesStack[self.valuesStack.__len__() - 1][2].__str__())
        self.bbottomField.setText(self.valuesStack[self.valuesStack.__len__() - 1][3].__str__())

    def setupDefaultValues(self):
        """
        Sets up default settings.
        """
        self.ttopField.setText(self.genUCut.__str__())
        self.tbottomField.setText(self.genLCut.__str__())
        self.btopField.setText(self.genAngInc.__str__())
        self.bbottomField.setText(self.genRadStep.__str__())

    @pyqtSlot()
    def make_change(self):
        """
        Read the input values from the text fields and sends them to fiberfit.py as a signal
        """
        uCut = float(self.ttopField.text())
        lCut = float(self.tbottomField.text())
        angleInc = float(self.btopField.text())
        radStep = float(self.bbottomField.text())
        self.valuesStack.append((uCut, lCut, angleInc, radStep))
        self.sendValues.emit(uCut, lCut, angleInc, radStep)

    @pyqtSlot()
    def do_change(self):
        """
        This is a slot that's connected to Settings button of the main UI.
        """
        self.exec_()
