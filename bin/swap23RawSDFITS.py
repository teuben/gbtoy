#! /usr/bin/env python
#
#2019.02.05 Frayer
#Python 3.7.2
#IPython 7.2.0

__doc__ = """
Swapping the RA and DEC positions for Argus beam 2 and 3 due to
cable mis-match for Argus data taken before 2018.10.22 19:30 UT

This program assumes input is raw SDFITS files 
where scan and integration numbers are in the exact same order
between beams.   If this is not the case or not sure, then should
loop through unqiue scan numbers and integration numbers and
replace individual records which would be much slower.
Beam 2 and Beam 3 data are in different VEGAS banks so need to read
in the C and D bank VEGAS files 

SDFITS files for the GBT are large tables stored in extension=1 where
each row represents a specific interation number, scan number,
spectral window, beam number, frequency-state, subreflector-state,
and other states/parameters that are used by other instruments (83
columns)


Usage: % swap23RawSDFITS.py raw.vegas.C.fits  raw.vegas.D.fits
or     % swap23RawSDFITS.py raw.vegas
where the latter mode will append ".C.fits" and ".D.fits"

Warning: Replaces data in original input files
"""

#
#
from astropy.io import fits 
import sys
import numpy as np

if len(sys.argv) == 0:
    print(__doc__)
    sys.exit(0)

if len(sys.argv) == 2:
    FileC = sys.argv[1] + '.C.fits'
    FileD = sys.argv[1] + '.D.fits'
else:
    FileC = sys.argv[1]
    FileD = sys.argv[2]


#fileC 
tabC=fits.getdata(FileC,ext=1)
hC=fits.getheader(FileC,ext=1)
raC = tabC["CRVAL2"]
decC = tabC["CRVAL3"]
feedC = tabC["FEED"]
nraC=np.copy(raC)
ndecC=np.copy(decC)

#fileD
tabD=fits.getdata(FileD,ext=1)
hD=fits.getheader(FileD,ext=1)
raD = tabD["CRVAL2"]
decD = tabD["CRVAL3"]
feedD = tabD["FEED"]
nraD=np.copy(raD)
ndecD=np.copy(decD)

#Beam-3 is in C Bank and Beam-2 is in D Bank
id2=np.where(feedD==2)
id3=np.where(feedC==3)
idx2=id2[0]
idx3=id3[0]

#swap indices
nraD[idx2]=raC[idx3]
nraC[idx3]=raD[idx2]
ndecD[idx2]=decC[idx3]
ndecC[idx3]=decD[idx2]

#replace values
tabD["CRVAL2"]=nraD
tabD["CRVAL3"]=ndecD
tabC["CRVAL2"]=nraC
tabC["CRVAL3"]=ndecC

#leave our marks, and be stubborn
if 'SWAP23' in hC:
    print("Error: it seems %s was already SWAP23-ed" % FileC)
    sys.exit(1)
if 'SWAP23' in hD:
    print("Error: it seems %s was already SWAP23-ed" % FileD)
    sys.exit(1)    
hC['SWAP23'] = True
hD['SWAP23'] = True

#update input files
fits.update(FileC,tabC,hC,ext=1)
fits.update(FileD,tabD,hD,ext=1)

#inform
print("Overwritten %s and %s" % (FileC,FileD))
