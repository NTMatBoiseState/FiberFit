from __future__ import print_function
import numpy as np
from skimage import io, filters
from quanfima.quanfima import morphology as mrph
from quanfima.quanfima import visualization as vis
from quanfima.quanfima.visualization_testQ import plot_orientation_test_map
from quanfima.quanfima import utils2
#from quanfima.quanfima import utils
from skimage.morphology import watershed
from skimage.feature import peak_local_max
from skimage import measure
from skimage.segmentation import random_walker
import matplotlib.pyplot as plt
from scipy import ndimage
import matplotlib.pyplot as plt
from skimage import data
from skimage.filters import threshold_otsu
import cv2
import math
import time
import os
import itertools
import numpy as np
from skimage import feature, measure, filters
from skimage.util.shape import view_as_blocks
from scipy import ndimage as ndi
from scipy.spatial import distance
import vigra
import pandas as pd
from multiprocessing import Pool
from quanfima.quanfima import cuda_available

if cuda_available:
    import pycuda.autoinit
    import pycuda.driver as cuda
    from pycuda.compiler import SourceModule
    from pycuda import gpuarray


def colormaps(orient_type,paddding=20,diameter_window_radius=12,window_radius=12):
    img = cv2.imread('Data/segmented_square.png',0)
    #img = np.invert(img)
    #img_seg = img
    #plt.imshow(img)
    binary = img #>125
    #plt.imshow(binary)
    img_seg=binary
    #binary.ndim
    skeleton = img_seg
    data = skeleton
    skeleton_thick=skeleton
    #plt.imshow(skeleton)
    fiber_mask= data
    fiber_skel = skeleton
    #paddding=50
    #window_radius=12,
    #orient_type='pca'
    #diameter_window_radius=12 
    orientation_vals, diameter_vals = [], []

    padded_fiber_skel = np.pad(fiber_skel, pad_width=(paddding,), mode='constant', constant_values=0)
    padded_fiber_mask = np.pad(fiber_mask, pad_width=(paddding,), mode='constant', constant_values=0)
    #plt.imshow(padded_fiber_skel)
    pcy, pcx = (10*2+1)/2., (10*2+1)/2.

    ycords, xcords = np.nonzero(padded_fiber_skel)

    clear_padded_fiber_skel = padded_fiber_skel.copy()
    method = feature.corner_harris(clear_padded_fiber_skel, sigma=1)#sigma=1.5
    #plt.imshow(method)
    corner_points = feature.corner_peaks(method, min_distance=1)#min_distance =3
    image = img
    #fig = plt.figure()
    #plt.imshow(image)
    # Convert coordinates to x and y lists
    #y_corner,x_corner = zip(*corner_points)
    #plt.plot(x_corner,y_corner,'o') # Plot corners
    #if title:
        #plt.title('title')
    #plt.xlim(0,data.shape[1])
    #plt.ylim(data.shape[0],0) # Images use weird axes
    #fig.set_size_inches(np.array(fig.get_size_inches()) * 1.5)
    #plt.show()
    #print "Number of corners:",len(corners)
    for i, (yy, xx) in enumerate(corner_points):
        clear_padded_fiber_skel[yy-2:yy+4, xx-2:xx+4] = np.zeros((6, 6),
                                           dtype=clear_padded_fiber_skel.dtype)
    from quanfima.quanfima import morphology7 as mrph
    cskel, fskel, omap, dmap, ovals, dvals = \
                            mrph.estimate_fiber_properties(data, skeleton)
    #plt.imshow(clear_padded_fiber_skel)
    from quanfima.quanfima.visualization_testQ import plot_orientM_map, plot_orientation_test_map
    # plot results
    plot_orientM_map(omap, cskel, min_label=u'0°', max_label=u'180°',
                             figsize=(10,10),
                             name='2d_polymer',
                             output_dir='output/')
    vis.plot_diameter_map(dmap, cskel, figsize=(10,10), cmap='gist_rainbow',
                      name='2d_polymer',
                      output_dir='/path/to/output/dir')
