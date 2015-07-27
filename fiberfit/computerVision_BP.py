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

from fiberfit.EllipseDirectFit import *  # XXX: Changed here
from fiberfit.helpers import *  # XXX: Changed here

figSize = 4.5


def process_histogram(PabsFlip, N1):
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #           Create orientation Histogram         %
    #    Sum pixel intensity along different angles  %
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    n1 = np.round(N1 / 2) - 1
    freq = np.arange(-n1, n1 + 1, 1)
    x, y = freq, freq

    #  Set up polar coordinates prior to summing the spectrum
    theta1Rad = np.linspace(0.0, 2 * math.pi, num=360)
    f1 = np.round_(N1 / (2 * 32.0))
    f2 = np.round_(N1 / (2 * 2))

    rho1 = np.linspace(f1, f2, num=(f2 - f1) * 2)  # frequency band
    PowerX = np.zeros((theta1Rad.size, theta1Rad.size))
    PowerY = np.zeros((theta1Rad.size))

    # Interpolate using a Spine
    PowerSpline = scipy.interpolate.RectBivariateSpline(y=y, x=x, z=PabsFlip)
    n_dx = 0.001

    for p in range(0, theta1Rad.size):
        # converting theta1Rad and rho1 to cartesian coordinates
        xfinal = rho1 * math.cos(theta1Rad[p])
        yfinal = rho1 * math.sin(theta1Rad[p])

        # Evaluate spin on path
        px = PowerSpline.ev(yfinal, xfinal)
        PowerY[p] = np.sum(px)

    # Only use the data in the first two quadrants (Spectrum is symmetric)
    num = len(theta1Rad)
    PowerYFinal = PowerY[0:num // 2]
    theta1RadFinal = theta1Rad[0:num // 2]
    # theta1DegFinal = theta1Deg[0:num/2]

    power_area = np.trapz(PowerYFinal, theta1RadFinal)
    normPower = PowerYFinal / power_area

    # % Elliptical Method to find orientation (EllipseDirectFit.m)
    # Determine mean location using elliptic method (EllipseDirectFit.m)
    # num_angles=length(theta1DegFinal)

    return normPower, theta1RadFinal


def process_ellipse(normPower, theta1RadFinal):
    # Combine data into [XY] to fit to an ellipse
    Mirtheta1RadFinal1 = np.concatenate([theta1RadFinal.T, (theta1RadFinal + np.pi).T])
    MirnormPower = np.concatenate([normPower.T, normPower.T])

    # Convert mirrored polar coords to cartesian coords
    xdata, ydata = pol2cart(Mirtheta1RadFinal1, MirnormPower)
    ell_data = np.vstack([xdata, ydata])
    ell_data = ell_data.T

    # Python fitting function, see EllipseDirectFit
    A, centroid = EllipseDirectFit(ell_data)
    t = orientation(A)

    # Plot Lower Left - Polar plot of angular distribution
    angDist = plt.figure(figsize=(figSize, figSize))  # Creates a figure containing angular distribution.
    r_line = np.arange(0, max(MirnormPower) + .5, .5)
    th = np.zeros(len(r_line))
    for i in range(0, len(r_line)):
        th[i] = t
    th = np.concatenate([th, (th + 180)])
    r_line = np.concatenate([r_line, r_line])
    plt.polar(Mirtheta1RadFinal1, MirnormPower, linewidth=2)
    plt.polar(th * pi / 180, r_line, color='r', linewidth=3)
    plt.yticks(np.arange(.5, max(MirnormPower), .5))
    angDist.savefig('angDist')
    plt.close()

    return t, angDist


def process_kappa(t_final, theta1RadFinal, normPower):
    t_final_rad = t_final * pi / 180

    def fitted_func(thetas, c):
        int_value, int_err = scipy.integrate.quadrature(func=lambda x: exp(c * cos(x)), a=0.0, b=np.pi)
        return ((np.pi * (1.0 / np.pi * (int_value))) ** - 1) * \
               np.exp(c * np.cos(2 * (thetas - t_final_rad)))

    c0 = 15
    kappa, kappa_pcov = scipy.optimize.curve_fit(f=fitted_func, p0=(c0,), xdata=theta1RadFinal, ydata=normPower)

    # Shift data for plotting purposes
    t = t_final

    diff = abs(theta1RadFinal - (t * pi / 180))
    centerLoc = find(diff == min(diff))

    num_angles = len(theta1RadFinal)
    shift = (round(num_angles / 2) - (num_angles - centerLoc))

    normPower1 = np.roll(normPower, -shift)
    theta1RadFinal1 = np.roll(theta1RadFinal, -shift)

    s = (num_angles - shift) + 1

    if (shift > 0):
        s = num_angles - shift + 1
        for k in range(s, num_angles):
            theta1RadFinal1[k] = pi + theta1RadFinal1[k]
    elif (shift < 0):
        for k in range(0, -shift):
            theta1RadFinal1[k] = -pi + theta1RadFinal1[k]

    # Plot Lower Right - Distribution on a cartesian plane with appropriate shift
    cartDist = plt.figure(figsize=(figSize, figSize))  # Creates a figure containing cartesian distribution.

    h2 = plt.bar((theta1RadFinal1 * 180 / pi), normPower1)
    plt.xticks(np.arange(-180, 180, 45))
    plt.xlim([t - 100, t + 100])
    p_act = fitted_func(theta1RadFinal1, kappa)
    h3, = plt.plot(theta1RadFinal1 * 180 / pi, p_act, label='Pred VM Dist', linewidth=3)
    plt.title('Angular Distribution')
    plt.xlabel('Angle (Degrees)')
    plt.ylabel('Normalized Intensity')
    plt.legend(handles=[h3], loc=2)
    plt.yticks(np.arange(0, max(normPower1) + .3, .5))
    plt.ylim([0, max(normPower1) + .3])
    cartDist.savefig('cartDist')
    plt.close()

    return kappa, cartDist


def process_image(name):
    # %
    #  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #  FFT // POWER SPECTRUM // ANGULAR DISTRIBUTION
    #  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #  SIMPLE FFT
    #  %%%%%%%%%%%%%%%%%%%%%E%%%%%%%%%%%%%%%%
    im = scipy.ndimage.imread(fname=str(name))

    m, n = im.shape

    # Remove a row and column if the dimension of the image is odd
    if (m % 2 == 1):
        im = np.delete(im, (0), axis=0)
    if (n % 2 == 1):
        im = np.delete(im, (0), axis=1)

    # Plot Upper left - Original Image
    originalImage = plt.figure(frameon=False, figsize=(figSize, figSize))
    # Makes it so the image fits entire dedicated space.
    ax = plt.Axes(originalImage, [0., 0., 1., 1.])
    ax.set_axis_off()
    originalImage.add_axes(ax)
    plt.imshow(im, cmap='gray', aspect='auto')
    plt.axis('off')
    originalImage.savefig('orgImg')
    plt.close()

    fft_result = np.fft.fft2(im)
    Fshift = np.fft.fftshift(fft_result)
    Pabs = np.abs(Fshift) ** 2

    # shift in terms of image because power specrum is the mirroR of lines so
    # misrroring back in terms of image would give right allignment
    PabsFlip1 = np.rot90(Pabs)
    PabsFlip = np.flipud(PabsFlip1)
    PabsFlip = np.delete(PabsFlip, (0), axis=0)
    PabsFlip = np.delete(PabsFlip, (0), axis=1)

    # Plot Upper Right - Power Spectrum on logrithmic scale
    logScale = plt.figure(frameon=False, figsize=(figSize, figSize))
    # Makes it so the image fits entire dedicated space.
    ax = plt.Axes(logScale, [0., 0., 1., 1.])
    ax.set_axis_off()
    logScale.add_axes(ax)
    plt.axis('off')
    plt.imshow(log(PabsFlip), cmap='gray', aspect='auto')
    logScale.savefig('logScl')
    plt.close()

    M, N1 = im.shape

    normPower, theta1RadFinal = process_histogram(PabsFlip, N1)

    # theta and angular distribution are getting retrieved.
    t_final, angDist = process_ellipse(normPower, theta1RadFinal)

    # k and cartesian distrubution are getting retrieved.
    k, cartDist = process_kappa(t_final, theta1RadFinal, normPower)

    # Rounding results for Title of Figure
    krnd = math.ceil(k * 1000) / 1000
    thrnd = math.ceil(t_final * 1000) / 1000
    krnd = math.trunc(krnd * 100) / 100
    thrnd = math.trunc(thrnd * 100) / 100

    return k[0], t_final, angDist, cartDist, logScale, originalImage


def pol2cart(theta, radius):
    xx = radius * np.cos(theta)
    yy = radius * np.sin(theta)

    return (xx, yy)


def orientation(A):
    if (abs(A[1]) < (1 * 10 ^ (-15))):
        if (A[0] <= A[2]):
            # Ellipse is horizontal
            angle = 0;
            major = sqrt(1 / A[0])
            minor = sqrt(1 / A[2])
        else:
            angle = np.pi / 2;
            major = sqrt(1 / A[2])
            minor = sqrt(1 / A[0])
    else:
        R = ((A[2] - A[0]) / A[1])
        tg = R - sqrt((R * R) + 1)
        angle = math.atan(tg)
        P = (2 * tg) / (1 + (tg * tg))

        if ((A[0] > 0 and A[1] > 0 and A[2] > 0)):
            if (angle < (-pi / 4)):
                angle = angle + np.pi
            else:
                angle = angle
        elif ((A[1] / P <= (-A[1] / P))):
            if (angle < 0):
                angle = angle + np.pi / 2
            else:
                angle = angle - np.pi / 2
        elif (A[0] < 0 and A[1] < 0 and A[2] < 0):
            if (angle < 0):
                angle = angle + np.pi
            else:
                angle = angle - np.pi
        else:
            # Switch
            if (angle < 0):
                angle = angle + np.pi / 2
            else:
                angle = angle - np.pi / 2

    t_New = angle * 180 / np.pi

    return (t_New)
