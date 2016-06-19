## Overview
FiberFit is a portable Python application for Mac and Windows. It uses computer vision to analyze 2-D 8-bit images. Code is hosted in a private repository on Bitbucket. The bulk of my work included making a Graphical User Interface (GUI) around an existing algorithm mentioned above. I used an Object-Oriented approach and built the application using the Model-View-Controller architectural pattern.

## Features
* Processes multiple images
* Exports result of the analysis in PDF (utilizes open-source Python library) and csv
* Live progress bar, which updates user about status of the image analysis (utilizes threading)

## Building and Running
You will need Python 3, pyqt5, pyPDF2, scipy, numpy, matplotlib, pandas and Ordered Set installed. Please checkout 
their respective sites to get instructions on how to install those libraries (e.g. via pip).
* [Python 3] (https://www.python.org/download/releases/3.4.0/)
* [PyQt5] (http://pyqt.sourceforge.net/Docs/PyQt5/installation.html)
* [PyPDF2] (https://pypi.python.org/pypi/PyPDF2/1.26.0)
* [scipy] (https://www.scipy.org/) 
* [numpy] (http://www.numpy.org/)
* [matplotlib] (http://matplotlib.org/)
* [pandas] (http://pandas.pydata.org/)
* [Ordered Set] (http://orderedset.readthedocs.io/en/latest/installation.html)

After you've installed required software above, run the following from ```fiberfit``` directory:
 1. export PYTHONPATH='.'
 1. python src/fiberfit_control/fiberfit.py

## Get Started
TODO: include get started documentation from NTM drive
Please check out a video demostration of FiberFit in action:
<iframe  title="FiberFit demo" width="480" height="390" src="https://www.youtube.com/watch?v=ZIm1AxTubYo" frameborder="0" allowfullscreen></iframe> 

## Deployment
cx_Freeze is a recommended tool for deploying FiberFit as a single cross-platform executable application. 
Please check out cx_Freeze[here] (http://cx-freeze.sourceforge.net/).

## Support
Primary developer - Aza Tulepbergenov (https://github.com/atulep)
Please contact NTM Labs for any questions.

