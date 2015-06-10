# from __future__ import print_function
# from __future__ import unicode_literals
# from __future__ import division
# from __future__ import absolute_import

import matplotlib
# matplotlib.use('Agg')

import numpy as np
import scipy
import scipy.ndimage
import scipy.interpolate
import scipy.optimize
import scipy.integrate
import math
import glob
from pylab import *
from pandas import DataFrame
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

# from matplotlib.patches import Ellipse

# from __future__ import division
# try:
#     from runtime import *
# except ImportError:
#     from smop.runtime import *

from fiberfit.EllipseDirectFit import * # XXX: Changed here
from fiberfit.helpers import * # XXX: Changed here

def process_histogram(PabsFlip, N1):

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #           Create orientation Histogram         %
    #    Sum pixel intensity along different angles  %
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    n1 = np.round(N1 / 2)-1
    freq = np.arange(-n1,n1+1,1)
    x,y = freq, freq

    #  Set up polar coordinates prior to summing the spectrum
    theta1Rad=np.linspace(0.0, 2*math.pi , num = 360)
    f1 = np.round_(N1/(2*32.0))
    f2 = np.round_(N1/(2*2))

    rho1=np.linspace(f1, f2, num = (f2-f1)*2) # frequency band
    PowerX=np.zeros((theta1Rad.size,theta1Rad.size))
    PowerY=np.zeros((theta1Rad.size))

    # Interpolate using a Spine
    PowerSpline = scipy.interpolate.RectBivariateSpline(y=y, x=x,z=PabsFlip)
    n_dx = 0.001

    for p in range(0,theta1Rad.size):
        # converting theta1Rad and rho1 to cartesian coordinates
        xfinal = rho1 * math.cos(theta1Rad[p])
        yfinal = rho1 * math.sin(theta1Rad[p])

        # Evaluate spin on path
        px = PowerSpline.ev(yfinal, xfinal)
        PowerY[p] = np.sum(px)

    # Only use the data in the first two quadrants (Spectrum is symmetric)
    num=len(theta1Rad)
    PowerYFinal = PowerY[0:num//2]
    theta1RadFinal = theta1Rad[0:num//2]
    # theta1DegFinal = theta1Deg[0:num/2]

    power_area = np.trapz( PowerYFinal, theta1RadFinal )
    normPower = PowerYFinal / power_area

    # % Elliptical Method to find orientation (EllipseDirectFit.m)
    # Determine mean location using elliptic method (EllipseDirectFit.m)
    # num_angles=length(theta1DegFinal)

    return normPower, theta1RadFinal


def process_ellipse(normPower, theta1RadFinal):

    # Combine data into [XY] to fit to an ellipse
    Mirtheta1RadFinal1=np.concatenate([theta1RadFinal.T,(theta1RadFinal + np.pi).T])
    MirnormPower=np.concatenate([normPower.T,normPower.T])

    # Convert mirrored polar coords to cartesian coords
    xdata,ydata=pol2cart(Mirtheta1RadFinal1,MirnormPower)

    ell_data = np.vstack([xdata,ydata])
    ell_data = ell_data.T

    # Python fitting function, see EllipseDirectFit
    A, centroid=EllipseDirectFit(ell_data)

    t = orientation(A)

    #Plot Lower Left - Polar plot of angular distribution
    plt.subplot(223, polar = True)

    r_line = np.arange(0, max(MirnormPower)+.5, .5)
    th = np.zeros(len(r_line))
    for i in range (0, len(r_line)):
        th[i] = t
    th = np.concatenate([th, (th+180)])
    r_line = np.concatenate([r_line, r_line])

    plt.polar(Mirtheta1RadFinal1, MirnormPower, linewidth = 2)
    plt.polar(th*pi/180, r_line, color = 'r', linewidth = 3)
    plt.yticks(np.arange(.5, max(MirnormPower), .5))
    #plt.title('Angular Distribution') upon Rici's request

    return t

def process_kappa(t_final, theta1RadFinal, normPower):

    t_final_rad=t_final * pi / 180

    def fitted_func(thetas, c):

        int_value, int_err = scipy.integrate.quadrature(func=lambda x: exp(c * cos(x)), a=0.0, b=np.pi)

        return ((np.pi * ( 1.0/np.pi * ( int_value ))) ** - 1) * \
            np.exp(c * np.cos(2 * (thetas - t_final_rad)))

    c0=15
    kappa, kappa_pcov = scipy.optimize.curve_fit(f=fitted_func,p0=(c0,), xdata=theta1RadFinal, ydata=normPower)

    #Shift data for plotting purposes

    t = t_final

    Diff = abs(theta1RadFinal-(t*pi/180))
    centerLoc = find(Diff==min(Diff))

    num_angles = len(theta1RadFinal)
    shift = (round(num_angles/2)-(num_angles-centerLoc))

    normPower1 = np.roll(normPower, -shift)
    theta1RadFinal1 = np.roll(theta1RadFinal, -shift)

    s = (num_angles-shift)+1

    if (shift > 0):
        s=num_angles-shift+1
        for k in range(s, num_angles):
            theta1RadFinal1[k]=pi+theta1RadFinal1[k]
    elif (shift < 0):
        for k in range(0,-shift):
            theta1RadFinal1[k]=-pi+theta1RadFinal1[k]

    #Plot Lower Right - Distribution on a cartesian plane with appropriate shift

    plt.subplot(224)
    h2 = plt.bar((theta1RadFinal1*180/pi), normPower1)
    plt.xticks(np.arange(-180, 180, 45))
    plt.xlim([t-100, t+100])

    p_act = fitted_func(theta1RadFinal1, kappa)
    subplot(224)
    h3, = plt.plot(theta1RadFinal1*180/pi, p_act, label = 'Pred VM Dist', linewidth = 3)
    plt.title('Angular Distribution')
    plt.xlabel('Angle (Degrees)')
    plt.ylabel('Normalized Intensity')
    plt.legend(handles = [h3], loc = 2)
    plt.yticks(np.arange(0, max(normPower1)+.3, .5))
    plt.ylim([0, max(normPower1)+.3])

    return kappa

def process_image(name, ii):

    # %
    #  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #  FFT // POWER SPECTRUM // ANGULAR DISTRIBUTION
    #  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #  SIMPLE FFT
    #  %%%%%%%%%%%%%%%%%%%%%E%%%%%%%%%%%%%%%%

    im = scipy.ndimage.imread(fname=str(name))

    m,n = im.shape

    # Remove a row and column if the dimension of the image is odd
    if (m%2 == 1):
        im = np.delete(im, (0), axis = 0)
    if (n%2 == 1):
        im = np.delete(im, (0), axis = 1)

    #Plot Upper left - Original Image
    fig = figure(ii, figsize = (7.5,6), facecolor = 'white')

    plt.subplot(221)
    plt.imshow(im, cmap = 'gray')
    plt.axis('off')

    fft_result = np.fft.fft2(im)
    Fshift=np.fft.fftshift(fft_result)
    Pabs=np.abs(Fshift) ** 2
    #  shift in terms of image because power specrum is the mirroR of lines so
    #  misrroring back in terms of image would give right allignment
    PabsFlip1=np.rot90(Pabs)
    PabsFlip=np.flipud(PabsFlip1)

    PabsFlip = np.delete(PabsFlip, (0), axis=0)
    PabsFlip = np.delete(PabsFlip, (0), axis=1)

    #Plot Upper Right - Power Spectrum on logrithmic scale
    plt.subplot(222)
    plt.axis('off')
    plt.imshow(log(PabsFlip), cmap = 'gray')

    M,N1=im.shape

    normPower, theta1RadFinal = process_histogram(PabsFlip, N1)

    t_final = process_ellipse(normPower, theta1RadFinal)
    print("theta_p", t_final)

    k = process_kappa(t_final, theta1RadFinal, normPower)
    print("kappa:", k)

    #Rounding results for Title of Figure
    krnd = math.ceil(k*1000)/1000
    thrnd = math.ceil(t_final*1000)/1000
    krnd = math.trunc(krnd*100)/100
    thrnd = math.trunc(thrnd*100)/100

    fig.suptitle('%s \n' %(name.lstrip('/Users/azatulepbergenov/PycharmProjects/fiberfit/test/')), fontsize = 14)
    #fig.suptitle('%s \n\n k = %s   mu = %s degrees \n\n' %(name.lstrip('/Users/azatulepbergenov/PycharmProjects/fiberfit/test/'), krnd, thrnd), fontsize = 14, fontstyle = 'italic')
    return k, t_final

def pol2cart(theta, radius):

     xx = radius*np.cos(theta)
     yy = radius*np.sin(theta)

     return (xx,yy)

def orientation(A):

    if(abs(A[1]) < (1*10^(-15))):
        if(A[0] <= A[2]):
            # Ellipse is horizontal
            angle = 0;
            major = sqrt(1/A[0])
            minor = sqrt(1/A[2])
        else :
            angle = np.pi/2;
            major = sqrt(1/A[2])
            minor = sqrt(1/A[0])
    else:
        R = ((A[2]-A[0])/A[1])
        tg = R-sqrt((R*R)+1)
        angle = math.atan(tg)
        P = (2*tg)/(1+(tg*tg))

        if((A[0]>0 and A[1] >0 and A[2] >0)):
            if(angle < (-pi/4)):
                angle = angle + np.pi
            else:
                angle = angle
        elif((A[1]/P <= (-A[1]/P))):
            if(angle < 0):
                angle = angle + np.pi/2
            else:
                angle = angle - np.pi/2
        elif (A[0]<0 and A[1] <0 and A[2] <0):
            if(angle < 0):
                angle = angle + np.pi
            else:
                angle = angle - np.pi
        else:
            #Switch
            if(angle < 0):
                angle = angle + np.pi/2
            else:
                angle = angle - np.pi/2

    t_New = angle*180/np.pi

    return (t_New)


class fiberfit_model(object):

    def __init__(self):

        self.th = 0
        self.k = 0


    def setTh(self, th):
        self.th = th

    def setK(self, k):
        self.k = k

    def getTh(self):
        return self.th
    def getK(self):
        return self.k

    def main(self, files):

        # os.chdir('../test/')
        import pathlib
        from pathlib import Path


        #testdir = Path("../test/")
        #print("Testdir:", testdir.resolve().absolute())
        # Grab all of the images within the same folder as the code and initialize data arrays
        #files = list(testdir.glob("*.png"))

        #print("Files:", [ f.name for f in files ] )

        #name = np.zeros(1, dtype = object)
        #th = np.zeros(1)
        #k = np.zeros(1)

        #for ii in range(0,len(files)): # ii defines what image in the directory is being process
            ##TODO: Note, -3 is hardcoded - bad
        filename = files # Get file names
        Data = process_image(filename, self.numImages) # Sends image and image number to be processed through FFT
        name = filename.lstrip('/Users/azatulepbergenov/PycharmProjects/fiberfit/test/')
        th = Data[0] # Average Orientation of Fiber Network
        k = Data[1] # Concentration parameter, k
        fiberfit_model.setK(self, round(k, 2))
        fiberfit_model.setTh(self, round(th[0],2))
        #plt.show()
        plt.savefig("image" + str(self.numImages))

        df = DataFrame({'Image Name': name, 'Theta_p': th, 'Kappa': k})
        df.to_csv('Test1.csv', index = False)

if __name__ == '__main__':

    import timeit

    runtime = timeit.timeit(main, number=1)
    print("Ran in: %.3f s "%runtime)