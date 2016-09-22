## Overview
FiberFit is a portable Python application for Mac and Windows. It uses computer vision to analyze ligament patterns in 2-D 8-bit images. A results summary table (.csv) and image summary documents (.pdf) may be exported by the user. 
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
* [Qt Creater {optional}] (https://www.qt.io/download/)

After you've installed all of the items above, you can start the application by:
```python src/fiberfit_control/fiberfit.py```
**Note**, the above command assumes you are inside of FiberFit/ folder.

## Get Started
Please check out a video demostration of FiberFit in action [HERE](https://www.youtube.com/watch?v=ZIm1AxTubYo)

## Deployment
cx_Freeze is a recommended tool for deploying FiberFit as a single cross-platform executable application. 
Please check out cx_Freeze[here] (http://cx-freeze.sourceforge.net/). Note that, working setup.py is included in the root directory.

## Support
Primary developer - Aza Tulepbergenov (https://github.com/atulep)

Please contact NTM Labs for any questions.

