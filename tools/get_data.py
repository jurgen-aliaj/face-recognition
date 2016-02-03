#!/usr/bin/env python
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import random
import time
from scipy.misc import imsave
from scipy.misc import imread
from scipy.misc import imresize
import matplotlib.image as mpimg
import os
from scipy.ndimage import filters
import urllib


act = ['Gerard Butler', 'Daniel Radcliffe', 'Michael Vartan', 'Lorraine Bracco', 'Peri Gilpin', 'Angie Harmon']
#act = list(set([a.split("\t")[0] for a in open("subset_actors.txt").readlines()]))


def timeout(func, args=(), kwargs={}, timeout_duration=1, default=None):
    '''From:
    http://code.activestate.com/recipes/473878-timeout-function-using-threading/'''
    import threading
    class InterruptableThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = None

        def run(self):
            try:
                self.result = func(*args, **kwargs)
            except:
                self.result = default

    it = InterruptableThread()
    it.start()
    it.join(timeout_duration)
    if it.isAlive():
        return False
    else:
        return it.result

def rgb2gray(rgb):
    '''Return the grayscale version of the RGB image rgb as a 2D numpy array
    whose range is 0..1
    Arguments:
    rgb -- an RGB image, represented as a numpy array of size n x m x 3. The
    range of the values is 0..255
    '''
    
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray/255.

testfile = urllib.URLopener()            


#Note: you need to create the uncropped folder first in order 
#for this to work

for a in act:
    name = a.split()[1].lower()
    i = 0
    line_number = 0
    for line in open("faces_subset.txt"):
	line_number += 1
        if a in line:
	    x = line.split()[-2].split(',')
	    x1, y1, x2, y2 = int(x[0]), int(x[1]), int(x[2]), int(x[3])
            del x
	    filename = name
	    if line_number >= 3168:
		filename += '_female_'
	    else:
		filename += '_male_'
            filename += str(i)+'.'+line.split()[4].split('.')[-1]
            #A version without timeout (uncomment in case you need to 
            #unsupress exceptions, which timeout() does)
            #testfile.retrieve(line.split()[4], "uncropped/"+filename)
            #timeout is used to stop downloading images which take too long to download
            timeout(testfile.retrieve, (line.split()[4], "uncropped/"+filename), {}, 30)
            
	    if not os.path.isfile("uncropped/"+filename):
                continue
		
 	    try:
		I = imread("uncropped/" + filename)
	    	I = I[y1:y2, x1:x2]
	    	I = rgb2gray(I)
            	I = imresize(I, (32, 32))
		if not isinstance(I[0][0], np.uint8):
			print 'no'
			print 2/0
	      	imsave("cropped/" + filename, I)
	    except Exception:
		os.remove("uncropped/" + filename)
		continue
            
            print filename
            i += 1
    
