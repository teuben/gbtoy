#!/usr/bin/env python
from astropy.io import fits
from astropy import units as u
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from astropy.visualization import quantity_support
from specutils import Spectrum1D, SpectrumList, SpectrumCollection

from astropy.io import ascii
from astropy.nddata import StdDevUncertainty
from astropy.table import Table
from astropy.units import Unit
from astropy.wcs import WCS
from astropy.convolution import convolve, Box1DKernel

from specutils.io import get_loaders_by_extension
from specutils.io.registers import data_loader
from specutils.io.parsing_utils import read_fileobj_or_hdulist
from specutils import Spectrum1D

def identify_sdfits(origin, *args, **kwargs):
    print("IDENTIFY_SDFITS - why is this never called?")
    try:
        # @todo use specutils.parsing. 
        with fits.open(args[0]) as hdulist:
            extname = hdulist[1].header['EXTNAME']
            if extname == 'SINGLE DISH':
                print("Hurray, we have SDFITS")
                return False
            else:
                print("Warning, skipping extname %s" % extname)
                return False
    except Exception as e:
        raise e

    
#@data_loader("sdfits", identifier=identify_sdfits, dtype=SpectrumList, extensions=['fits'],verbose=True)
@data_loader("sdfits", identifier=identify_sdfits, dtype=SpectrumCollection, extensions=['fits','sdfits'],verbose=True,priority=10)
def sdfits_loader(file_name, spectral_axis_unit=None, **kwargs):
    # just a few important ones for now, there are about 70 in the full SDFITS
    sdfits_headers = ['SCAN', 'PROCSEQN', 'CAL', 'OBJECT','SAMPLER', 'TCAL']
    spectra = []
    debug = kwargs.pop('debug',False)
    collection = kwargs.pop('collection',False)
    with read_fileobj_or_hdulist(file_name, **kwargs) as hdulist:
        header1= hdulist[0].header        
        header2= hdulist[1].header
        data   = hdulist[1].data
        nrow   = len(data)
        nchan  = 0
        for i in range(nrow):
            sp = data[i]['DATA']
            if nchan==0:
                nchan = len(sp)     # every spectrum in SDFITS has the same length
            crval1  = data[i]['CRVAL1']
            cdelt1  = data[i]['CDELT1']
            crpix1  = data[i]['CRPIX1']
            ctype1  = data[i]['CTYPE1']     # 'FREQ-OBS' to 'FREQ'; assuming SPECSYS='TOPOCENT'
            restfrq = data[i]['RESTFREQ']
            cunit1  = 'Hz'
            crval2  = data[i]['CRVAL2']
            crval3  = data[i]['CRVAL3']
            ctype2  = data[i]['CTYPE2']
            ctype3  = data[i]['CTYPE3']
            if ctype1 == 'FREQ-OBS': ctype1  = 'FREQ'
            # only axis1 needs a full description, axis2,3,4 are all single points
            wcs = WCS(header={'CDELT1': cdelt1, 'CRVAL1': crval1, 'CUNIT1': cunit1,
                              'CTYPE1': ctype1, 'CRPIX1': crpix1, 'RESTFRQ': restfrq,
                              'CTYPE2': ctype2, 'CRVAL2': crval2,
                              'CTYPE3': ctype3, 'CRVAL3': crval3})
                              

            meta = {}
            if debug:
                # adding the actual FITS headers is for debugging, but not in production mode
                meta['header1'] = header1
                meta['header2'] = header2
                #h = {**header1,**header2}
            else:
                for key in sdfits_headers:
                    if key in header1:
                        meta[key] = header1[key]
                    elif key in header2:
                        meta[key] = header2[key]
                    else:
                        meta[key] = data[i][key]    # why doesn't       key in data[i]    work?
                # add our row counter
                meta['_row'] = i
                        
        
            sp = sp * Unit('K')
            spec = Spectrum1D(flux=sp, wcs=wcs, meta=meta, velocity_convention="radio")
            spectra.append(spec)
            
    if collection:
        return SpectrumCollection.from_spectra(spectra)
    else:
        return  SpectrumList(spectra)

if __name__ == "__main__":
    fname = 'nb/ngc5291.sdfits'
    sl1 = SpectrumCollection.read(fname,format="sdfits",debug=False,collection=True)
    print(sl1[0].meta)
    print(f'Found {len(sl1)} spectra')
    print(type(sl1))
