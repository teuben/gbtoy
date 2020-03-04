#! /usr/bin/env python
#
#
#    experiments to see how to read a large SDFITS file and trim it in size
#    and free memory of the original unwanted rows
#
#    At the current state it's a mess. I can't get it to clear memory
#

import numpy as np
from astropy.io import fits
import copy
import time
from memory_profiler import profile

def pause(msg, delta=0):
    if delta==0: return 
    print(msg)
    time.sleep(delta)

@profile
def my_main(filename):

    hdu = fits.open(filename)
    header = hdu[0].header   
    bintable = hdu[1]

    header2  = bintable.header
    data2    = bintable.data
    # spectra  = data2[:]['DATA']
    # the next command will finally load in the data, the rest were just pointers/references
    srcs = np.unique(data2[:]['OBJECT'])
    scan = np.unique(data2[:]['SCAN'])
    ncols = header2['NAXIS1']
    nrows = len(data2)
    nflds = header2['TFIELDS']

    pause('Fully Loaded')

    if False:
        row0 = data2[0]
        print(type(row0))     # <class 'astropy.io.fits.fitsrec.FITS_record'>
        pause('row0')

    # if you hdu.close() and then close the bintable, data2 and spectra, memory is freed
    # if you zero those data, memory is not freed, until hdu.close()
    if False:
        hdu.close()
        pause("hdu.close()-0")
        del(bintable)
        pause("bintable")
        del(data2)
        pause("data2")


    # select first 1352 rows from the SDFITS
    wh1 = bintable.data[:]['OBJECT'] == 'MOON'       
    if False:
        idx = np.where(wh1)
        data2 = data2[idx]    # a view
        pause('MOON subsetted-idx')
    else:
        data2 = data2[wh1]
        pause('MOON subsetted-wh1')

    nrows = len(data2)

    if False:
        hdu.close()
        #del(spectra)
        del(bintable)
        pause('hdu.close()-1')


    # each row is about 17k (NAXIS1)
    # yet, each deepcopy of a row allocates 22MB

    # is this the horror we need to do ???
    data3 = np.empty(nrows, dtype=type(data2[0]))
    pause('data3-begin %d' % nrows,0.0)
    for i in range(nrows):
        data3[i] = copy.copy(data2[i])    # copy.deepcopy goes too deep and trashes memory
                                          # copy.copy doesn't seem to work at all, has references
    pause('data3-end',0.0)
    pause('nrows=%d' % nrows)

    if False:
        hdu.close()
        #del(spectra)
        del(bintable)
        del(data2)
        #del(data3)    # this would release the memory
        pause('hdu.close()-2')


    # data2 = bintable.data[wh1]
    # data2 = copy.deepcopy(bintable.data[wh1])
    data4 = copy.copy(bintable.data[wh1])
    #spectra  = data3[:]['DATA']
    # now data2 is nice and small, but bintable.data still exists
    # removing it doesn't help, data2 has a reference!

    # pause('copy bintable MOON subset')
    del(data4)


    if False:
        bintable=0
        wh1=0
        # this will close 3GB
        hdu.close()    
        header=0
        header2=0
        srcs=0
        scan=0
        ncols=0
        nrows=0
        nflds=0
        spectra=0
        data2=0      # this finally released 3GB



    pause("END")


my_main('AGBT15A_430_71.raw.vegas.A.fits') 
