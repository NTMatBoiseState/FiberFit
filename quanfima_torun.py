import numpy as np
from skimage import io, filters
import cv2
from quanfima.quanfima import morphology as mrph
from quanfima.quanfima import visualizationDE as vis
from quanfima.quanfima import visualization_testQ as visb 
import matplotlib.pyplot as plt
#img_seg = cv2.imread('Data/MAX_5p_10_2.tif',0)
from os import listdir
from os.path import isfile, join
import numpy
import cv2


def fiber_visualization():
    plt.ioff()
    mypath='Data/'
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    images = numpy.empty(len(onlyfiles), dtype=object)
    names = numpy.empty(len(onlyfiles), dtype=object)
    for n in range(0, len(onlyfiles)):
        images[n] = cv2.imread( join(mypath,onlyfiles[n]),0 )
        names[n]= (onlyfiles[n])
        img = numpy.empty(len(images), dtype=object)
    for n in range(0,len(images)):
        img_seg= images[n]
    data = img_seg
    skeleton = img_seg
    skeleton_thick = img_seg
    #skeleton, skeleton_thick = utils.prepare_data(img_seg)
    cskel, fskel, omap, dmap, ovals, dvals = \
                        mrph.estimate_fiber_properties(data, skeleton)
    # plot results
    vis.plot_diameter_map(dmap, cskel, figsize=(10,10), cmap='gist_rainbow',
                          name='DIAMETER_estimate',
                          output_dir='output/')
    vis.plot_orientation_map(omap, fskel, min_label=None, max_label=None,
                             figsize=(10,10),
                             name='ORIENTATION_estimate',
                             output_dir='output/')