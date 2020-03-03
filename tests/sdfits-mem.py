#! /usr/bin/env python
#

import numpy as np
from astropy.io import fits
import copy
import time

def pause(msg, delta=5):
    print(msg)
    time.sleep(delta)

hdu = fits.open('AGBT15A_430_71.raw.vegas.A.fits') 
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



# is this the horror we need to do ???
data3 = np.empty(nrows, dtype=type(data2[0]))
pause('data3-begin %d' % nrows,0.0)
for i in range(nrows):
    data3[i] = data2[i]    # a deepcopy goes too deep and trashes memory
pause('data3-end',0.0)
pause('nrows=%d' % nrows)

if True:
    hdu.close()
    #del(spectra)
    del(bintable)
    del(data2)
    #del(data3)
    pause('hdu.close()-2')


# data2 = bintable.data[wh1]
# data2 = copy.deepcopy(bintable.data[wh1])
#data3 = copy.copy(bintable.data[wh1])
#spectra  = data3[:]['DATA']
# now data2 is nice and small, but bintable.data still exists
# removing it doesn't help, data2 has a reference!

# pause('copy bintable MOON subset')


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
