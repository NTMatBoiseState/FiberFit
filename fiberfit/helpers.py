#!/usr/bin/env python2.7

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

import argparse, re, os, glob, sys, pprint, itertools
import inspect

import numpy as np


config = {
    'end'  : '\n',
    'fmt'  : '%s ',
    'sep'  : '->',
    'file' : None,
}


def debug( *args ):
    try:
        st = inspect.stack()[1]
        funcName = st[3]
        funcCallStr = st[4]

        # print('funcCallStr',funcCallStr)
        varnames = re.search('debug\((.*)\)', funcCallStr[0])
        varnames = varnames.groups()[0].split(',')

        # print(varnames, args)
        for n, v in zip(varnames, args):
            v_str = str(v)
            v_str = "`%s`"%v_str if v_str.count('\n') == 0 else v_str
            print(config['fmt']%(n.strip())+config['sep'], v_str, end=config['end'], file=config['file'])

    except Exception as err:
        # print('debug(...error...)')
        raise err



def pol2cart(theta, radius, units='deg'):
    """Convert from polar to cartesian coordinates

    **usage**:
        x,y = pol2cart(theta, radius, units='deg')
    """
    if units in ['deg', 'degs']:
        theta = theta*np.pi/180.0
    xx = radius*np.cos(theta)
    yy = radius*np.sin(theta)

    return xx, yy