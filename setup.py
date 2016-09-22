#!usr/local/bin/python3
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "orderedset", "PyPDF2", "PIL", "pylab", "numpy"], 
    "includes": [
        "sip", 
        "scipy.integrate.vode",
        "scipy.integrate.lsoda",
        "scipy.ndimage",
        "scipy.interpolate",
        "scipy.integrate.quadrature",
        "scipy.optimize",
        "scipy.special._ufuncs_cxx",
        "scipy.sparse.csgraph._validation",
        "PyQt5", 
        "PyQt5.QtWidgets", 
        "PyQt5.QtGui", 
        "PyQt5.QtCore",
        "PyQt5.QtWebKit",
    ], 
    "excludes": ["tkinter"], 
    "include_files": [
        "src/fiberfit_model/EllipseDirectFit.py", 
        "resources/images/",
        "resources/images/clearButton.png",
        "resources/images/open.png",
        "resources/images/settings.png",
        "resources/images/start-icon.png",
        "resources/images/export.png",
        "src/fiberfit_gui/settings_dialog.py", "src/fiberfit_gui/error_dialog.py", "src/fiberfit_gui/fiberfit_GUI.py", "src/fiberfit_model/helpers.py", "src/fiberfit_control/support/img_model.py", "src/fiberfit_control/support/report.py", "src/fiberfit_control/support/settings.py", "src/fiberfit_control/support/error.py", "src/fiberfit_gui/export_window.py"
    ]
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "FiberFit",
        version = "2.0",
        author = YOUR_NAME, # put your name here
        description = "FiberFit",
        options = {"build_exe": build_exe_options},
        executables = [Executable("src/fiberfit_control/fiberfit.py", base=base)])