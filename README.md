## Overview
FiberFit is a portable Python application for Mac and Windows. It uses computer vision to analyze 2-D 8-bit images. Code is hosted in a private repository on Bitbucket. The bulk of my work included making a Graphical User Interface (GUI) around an existing algorithm mentioned above. I used an Object-Oriented approach and built the application using the Model-View-Controller architectural pattern.

## TODO:
1. Need to simplify logic in  fiberfit.py as far as passing images around. I fixed minor issues, such as made sure that code works with current setup. But, would like to redesign the algorithm and eliminate dependency on indexes. Perhaps use dictionary.
2. Refactor the Main Window GUI part
3. Refactor the Settings etc
4. Refactor the computerVision.py

## Features
* Processes multiple images
* Exports result of the analysis in PDF (utilizes open-source Python library) and csv
* Live progress bar, which updates user about status of the image analysis (utilizes threading)

## Support
Primary developer - Aza Tulepbergenov (https://github.com/atulep)
Please contact NTM Labs for any questions.
