# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 22:35:58 2019

@author: abdul
"""

import glob
import h5py
import numpy as np
from scipy.signal import medfilt
import matplotlib.pyplot as plt

    
def extractImage(file, filterSize = 3):
    
    flatArray = file['/AwakeEventData/XMPP-STREAK/StreakImage/streakImageData'][()] 
    height = file['AwakeEventData/XMPP-STREAK/StreakImage/streakImageHeight'][()]
    width = file['/AwakeEventData/XMPP-STREAK/StreakImage/streakImageWidth'][()]
    
    rawImage = np.reshape(flatArray, (height[0],width[0]))
    filteredImage = medfilt(rawImage,filterSize)
    
    return rawImage, filteredImage
    
       
if __name__ == "__main__":
    

    with h5py.File(glob.glob("1541962108935000000_167_838.h5")[0],'r') as f:
        raw, filtered = extractImage(f)
        plt.imshow(filtered,interpolation='bicubic')
        plt.imsave('extractedImage.png',arr = filtered)