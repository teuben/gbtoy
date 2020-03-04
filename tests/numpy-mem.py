#! /usr/bin/env python
# allocate a big array, so we can see it in top

import numpy as np
import copy
import time
import psutil
from memory_profiler import profile


def pause(msg, delta=0):
    if delta==0: return
    print(msg)
    time.sleep(delta)

@profile
def my_main():

    a  = np.arange(1000*1000*200)
    pause('First a')

    # if you run top, you will see ipython sucking up 1.6GB
    # use the 'M' key to sort by memory usage

    a  = 0
    pause('a=0')


    # or del(a), but this will free up.
    # now do this again, but create some symlinks

    a = np.arange(1000*1000*200)
    a1 = a
    a2 = a[:]
    pause('Second a,a1,a2')

    # and free it

    a=0
    a1=0
    a2=0
    pause('a=a1=a2=0')

    # that worked fine. But here is a sequence that does NOT 
    # work and keeps the memory hostage

    a = np.arange(1000*1000*200)
    a1 = a
    a2 = a[:]
    pause('Third a,a1,a2')

    a=0          
    a1
    a1=0
    a2
    a2=0
    a
    a1
    a2
    pause('The weird a=a1=a2=0')

    # some variation on this theme did free memory. E.g. in python, 
    # instead of ipython, this sequence worked.   Replacing the
    # display of the 3 variables with a print() also worked. Go figure.

    a = np.arange(1000*1000*200)
    a1 = a
    a2 = a[:]
    a3 = copy.copy(a)
    a[0] = 999
    print('a3',a3[0])
    pause('Fourth a,a1,a2')

    a=0
    print(a1)
    a1=0
    print(a2)
    a2=0
    print(a)
    print(a1)
    print(a2)
    pause('The a=a1=a2=0 with print()')

    del(a3)
    
    pause('END')


my_main()
