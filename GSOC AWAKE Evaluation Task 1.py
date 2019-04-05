# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 20:43:40 2019

@author: abdul
"""

import glob
from datetime import datetime
from pytz import timezone
import pytz


def time(filename):

    '''
    Returns UTC human readable time and CERN(Zurich) Standard Time extracted from the name of 
    given h5 file.
    '''    
    nanoSecondsTime = int(glob.glob(filename)[0].split('.')[0].split('_')[0])
    
    Switzerland = timezone('Europe/Zurich')
    #Setting local timezone
    
    utc_dt = datetime.fromtimestamp(nanoSecondsTime // 1000000000, tz=pytz.utc) 
    #Diving by 1 million to convert it into millisecond range because datetime object can operate 
    #in millisecond precision.
    
    formt = '%Y-%m-%d %H:%M:%S %Z%z'
    #Print format
    
    zurich_dt = utc_dt.astimezone(Switzerland)
    
    return utc_dt.strftime(formt) ,zurich_dt.strftime(formt)

if __name__ == '__main__':
    utc, cern = time("*.h5")
    print('UTC time: ' + utc,'\nCERN time: ' + cern)