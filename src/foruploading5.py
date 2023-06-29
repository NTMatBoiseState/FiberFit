import io
import ipywidgets as widgets
import numpy
import cv2
import os
from os import listdir
from os.path import isfile, join
import numpy as np

def ff(b):
    for elem in b.new.values():
        #print(elem['metadata']['name'])
        with open(os.path.join('Data/',elem['metadata']['name']), 'wb') as file:
            file.write( elem['content'])

def upload(s):
    s.style.button_color = "lightblue"
    s.observe(ff, names='value')

def prepimages(mypath):
    ##Path to folder where you would like images to be saved
    savepath = 'output2/'
    ## Upload Files
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ];
    images = numpy.empty(len(onlyfiles), dtype=object);
    names = numpy.empty(len(onlyfiles), dtype=object);
    for n in range(0, len(onlyfiles)):
        images[n] = cv2.imread( join(mypath,onlyfiles[n]) );
        names[n]= (onlyfiles[n]);
    img_tot = numpy.empty(len(images), dtype=object);
    for n in range(0,len(images)):
        img_tot[n]= np.invert(images[n])
