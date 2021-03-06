from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

from matplotlib import pyplot as plt
import SimpleCV.ImageClass as scv

import scipy
import numpy as np
import cv2

class Kinect_infrared(object):

    def __init__(self):

        # Kinect runtime object, we want only depth and body frames
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Infrared|PyKinectV2.FrameSourceTypes_Depth) 
    
    def max_hist_depth(self, frame):    
        #print 'FRAME_MAX = ' + str(frame.max())
        binaries = int(frame.max())
        if binaries <= 0:
            return 0
        histogram, bins = np.histogram(frame, bins = binaries)
        histogram = histogram.tolist(); bins = bins.tolist(); 
        histogram[0 : 1] = [0, 0]
        max_hist = bins[histogram.index( max(histogram) )]
        return max_hist
    
    def run(self):

        
        print ':IN_RUN:Pulling Frames'

        while(True):
            #Main event loop
            if self._kinect.has_new_infrared_frame() or self._kinect.has_new_depth_frame:

                iframe = self._kinect.get_last_infrared_frame()
                iframe *= 1
                iframe = iframe.reshape(424,512)
                cv2.imshow('Infrared',iframe)

                dframe = self._kinect.get_last_depth_frame()
                dframe = dframe.reshape(424,512)
                dframe = np.array(dframe/16, dtype = np.uint8)
                gaussian_thresh = cv2.adaptiveThreshold(dframe, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,11,2)
                blur = cv2.GaussianBlur(dframe,(5,5),0)
                ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
                # dframe = cv2.findContours(dframe, mode = cv2.RETR_EXTERNAL, method = cv2.CHAIN_APPROX_NONE)
                cv2.imshow('Gaussian_thresh', gaussian_thresh)
                cv2.imshow('Gaussian_blur', blur)
                cv2.imshow('Gaussian_otsu', th3)



            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Close our Kinect sensor, close the window and quit.
        self._kinect.close()


HandGestureObject = Kinect_infrared();
HandGestureObject.run();