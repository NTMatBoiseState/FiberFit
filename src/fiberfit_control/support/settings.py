from PyQt5.QtWidgets import QDialogButtonBox, QDialog
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from src.fiberfit_gui import settings_dialog as SettingsDialog

class SettingsWindow(QDialog, SettingsDialog.Ui_Dialog):
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

    """
    Resets changes to the last saved changes.
    """

    def reset_changes(self):
        self.ttopField.setText(self.valuesStack[self.valuesStack.__len__() - 1][0].__str__())
        self.tbottomField.setText(self.valuesStack[self.valuesStack.__len__() - 1][1].__str__())
        self.btopField.setText(self.valuesStack[self.valuesStack.__len__() - 1][2].__str__())
        self.bbottomField.setText(self.valuesStack[self.valuesStack.__len__() - 1][3].__str__())

    """
    Sets up default settings.
    """

    def setupDefaultValues(self):
        self.ttopField.setText(self.genUCut.__str__())
        self.tbottomField.setText(self.genLCut.__str__())
        self.btopField.setText(self.genAngInc.__str__())
        self.bbottomField.setText(self.genRadStep.__str__())

    @pyqtSlot()
    def make_change(self):
        uCut = float(self.ttopField.text())
        lCut = float(self.tbottomField.text())
        angleInc = float(self.btopField.text())
        radStep = float(self.bbottomField.text())
        self.valuesStack.append((uCut, lCut, angleInc, radStep))
        self.sendValues.emit(uCut, lCut, angleInc, radStep)

    @pyqtSlot()
    def do_change(self):
        self.exec_()
