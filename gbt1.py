#!/usr/bin/env python

# taken from a notebook - 1-mar-2020

# # Some GBT CoDR experiments.
# 
# We implement some of the classes listed in V1.0 (Feb 2020) of the CoDR.   
# 
# * these are toy classes to show some of the functionality
# * not all member functions in all classes were implemented
# * very minimal error checking
# * some assumed organization of PS
# 
# This should eventually reproduce Example 1 (position switching) from
# the GBTIDL manual. The datafile **ngc5291.fits** you need is
# [here](http://safe.nrao.edu/wiki/pub/GB/Data/GBTIDLExampleAndSampleData/ngc5291.fits)
# or locally on **/n/chara/teuben/GBT**.  We will also show
# regressions values with the GBTIDL spectra.

# ## Example
# 
# We start off with a session as a GBT user might see this:
# 
#         ps = GBTLoadPS('a.fits')        # load the SDFITS file
#         ps.summary()                    # overview times, sources, scans etc.
#         ps.finalspectrum()              # calibrate and time/pol/scan average
#         ps.plot()                       # review the final plot 
#         ps.save('a1.fits')              # save the spectrum (also SDFITS format)
#         
# This is an example of a well behaved spectrum. No masking, no baseline fitting, just simple averaging. 
# 
# All the way at the end of this notebook these 5 lines will be reviewed again.

from astropy.io import fits
import numpy as np
import matplotlib
import copy
from matplotlib import pyplot as plt
from astropy.modeling import models, fitting


# # Spectrum
# 
# The class that contains one spectrum, something like Spectrum1D in specutils or Spectrum in pyspeckit. For now we are hardcoding the spectral axis in km/s, assuming the RESTFREQ is good. Doppler tracking ignored here for now.
# 


pjt1 = False
#pjt1 = True
# pjt1=True should give the same results as False, but it's not working yet


class Spectrum(object):
    """
    contains a basic spectrum
    not used by users
    """
    def __init__(self, sp):
        if pjt1 and type(sp) == Spectrum:
            self.data  = np.copy(sp.data)
            self.meta  = sp.meta
            self.gbt   = copy.deepcopy(sp.gbt)
            self.xvals = sp.xvals
        else:   
            # assume this is a bintable
            self.data  = sp['DATA']
            self.meta  = sp
            self.gbt  = {}
            # construct a freq axis in GHz
            nchan = len(self.data)        
            crval1 = sp['CRVAL1']
            cdelt1 = sp['CDELT1']
            crpix1 = sp['CRPIX1']
            freq0  = sp['RESTFREQ']/1e9
            freq   = (crval1 + (np.arange(1,nchan+1) - crpix1) * cdelt1)/1e9
            c = 299792.458 # km/s
            vel = (1-freq/freq0)*c
            self.xvals = vel
            # store RA,DEC
            if False:
                self.gbt['ra']  = sp['CRVAL2'] + sp['CDELT2'] * (sp['CRPIX2']-1)
                self.gbt['dec'] = sp['CRVAL3'] + sp['CDELT3'] * (sp['CRPIX3']-1)
            else:
                self.gbt['ra']  = sp['CRVAL2']
                self.gbt['dec'] = sp['CRVAL3']
            
    def __len__(self):
        return len(self.data)
        
        
    def stats(self, chans=None, edge=0, label=""):
        """
        show Mean,RMS,Min,Max
        """
        if chans==None:
            if edge == 0:
                c0 = 0
                c1 = len(self.data)
            else:
                c0 = edge
                c1 = -edge
        else:
            c0 = chans[0]
            c1 = chans[1]
        mean = self.data[c0:c1].mean()
        rms  = self.data[c0:c1].std()
        dmin = self.data[c0:c1].min()
        dmax = self.data[c0:c1].max()
        ndat = c1-c0
        print("%s  %s %s %s %s %d" %  (label,repr(mean),repr(rms),repr(dmin),repr(dmax),ndat))
        return (mean,rms,dmin,dmax,ndat)
    
    def flux(self, xrange=None, chans=None):
        """
        """
        dx = self.xvals[1]-self.xvals[0]
        if chans==None and xrange==None:
            flux = self.data.sum() * dx
        elif chans != None:
            c0 = chans[0]
            c1 = chans[1]
            flux = self.data[c0:c1].sum() * dx
        elif xrange != None:
            flux = 0
        else:
            flux = -1
        print("Flux %g" % flux)
        
    
    def plot(self, xrange=None, yrange=None, chans=None, label=None):
        """
        simple spectrum plot
        xrange and yrange are in physical units, e.g. xrange=[4500,5500]
        chans= are in channel numbers, e.g. chans=[2000,3000]
        """
        if xrange != None:   plt.xlim(xrange[0], xrange[1])
        if yrange != None:   plt.ylim(yrange[0], yrange[1])
        if chans == None:
            x = self.xvals
            y = self.data
        else:
            x = self.xvals[chans[0]:chans[1]]
            y = self.data[chans[0]:chans[1]]
        plt.plot(x,y)
        if 'bl' in self.gbt:
            if chans == None:
                bl = self.gbt['bl']
            else:
                bl = self.gbt['bl'][chans[0]:chans[1]]
            #print(type(x),type(bl))
            plt.plot(x,bl,'r-')          # plot full spectrum in red
            # plot the ranges...
            bl_chans = self.gbt['baseline']
            #print(bl_chans)
            for i in range(len(bl_chans)):    # loop over segments to plot in thick black
                c0 = bl_chans[i][0]
                c1 = bl_chans[i][1] 
                plt.plot(x[c0:c1],bl[c0:c1],'k-',linewidth=3)
            
        plt.xlabel("Velocity (km/s)")
        plt.ylabel("$T_A$ (K)")
        title = "Source: %s" % self.meta['OBJECT']
        if label != None:  title = title + " " + label
        plt.title(title)
        
    def smooth(self, win=11, method='hanning'):
        """
        win needs to be odd !!!
        method = ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']
        """
        data = np.copy(self.data)
        s=np.r_[data[win-1:0:-1],data,data[-2:-win-1:-1]]
        if method == 'flat':     # moving average
            w = np.ones(win,'d')
        else:
            w = eval('np.'+method+'(win)')
        data = np.convolve(w/w.sum(),s,mode='valid')
        w2 = (win-1)//2
        self.data = data[w2:-w2]
        
    def baseline(self, degree=2, chans=None, replace=False):
        """
        example      chans=[(1000,2000),(5000,6000)]
        """
        poly = models.Polynomial1D(degree=degree)
        fit = fitting.LinearLSQFitter()
        self.gbt['poly_degree'] = degree
        self.gbt['baseline'] = chans
        x = self.xvals
        y = np.copy(self.data)
        if chans != None:
            for i in range(len(chans)):
                c0 = chans[i][0]
                c1 = chans[i][1]
                #print("Segment",c0,c1)
                if i==0:
                    x0 = x[c0:c1]
                    y0 = y[c0:c1]
                else:
                    x0 = np.append(x0,x[c0:c1])
                    y0 = np.append(y0,y[c0:c1])
        else:
            x0 = x
            y0 = y          
        
        bl0 = fit(poly,x0,y0)
        if True:
            # residuals
            bl = bl0(x0) - y0
            print("Residuals[%d] %g %g" % (degree,bl.mean(),bl.std()))
        
        bl = bl0(x)
        #print(type(bl),type(x),type(bl))
        self.gbt['bl'] = bl
        if replace:
            self.data = self.data - bl
        
    def xy(self):
        """
        return spectrum
        """
        return (self.xvals, self.data)
             


# # SDFITSLoad
# 
# This is the class that loads an SDFITS file. Normally not called by users, but by classes such as GBTLoadPS()
# 
# 


class SDFITSLoad(object):
    """
    container for a bintable from a selected HDU
    normally not used by users
    """
    def __init__(self, filename, src=None, hdu=1):
        """
        """
        print("==SDFITSLoad %s" % filename)
        self.filename = filename
        self.bintable = None
        self.hdu = fits.open(filename)      # when to close?
        self.header = self.hdu[0].header
        self.load(src,hdu)
    def load(self, src=None, hdu=1):
        """
        for given hdu make this bintable available
        """
        self.bintable = self.hdu[hdu]
        self.header2  = self.bintable.header
        if src == None:
            self.data2    = self.bintable.data
        else:
            wh1 = self.bintable.data[:]['OBJECT'] == src
            if wh1.sum() == 0:
                srcs = np.unique(self.bintable.data[:]['OBJECT'])
                print("Warning: invalid source name",src," found",srcs)
                return
            self.data2 = self.bintable.data[wh1]
        self.spectra  = self.data2[:]['DATA']
        self.nchan    = len(self.data2[0]['DATA'])
        srcs = np.unique(self.data2[:]['OBJECT'])
        scan = np.unique(self.data2[:]['SCAN'])
        ncols = self.header2['NAXIS1']
        nrows = self.header2['NAXIS2']
        self.nrows = len(self.data2)
        nflds = self.header2['TFIELDS']
        restfreq = self.data2[0]['RESTFREQ']/1e9
        #
        print("File:     %s   HDU %d" % (self.filename, hdu))
        print("BINTABLE: %d rows x %d cols with %d chans" % (self.nrows,nflds,self.nchan))
        print("Selected %d/%d rows" % (self.nrows,nrows))
        print("Sources: ",srcs)
        print("RESTFREQ:",restfreq,'GHz')
        print("Scans:   ",scan)

    def __len__(self):
        return self.nrows
    
    def summary(self):
        print("WIP")
        

# # GBTLoad
# 
# This is the base class from which we derive all GBTLoad* subclasses that can load and calibrate spectra. It can also be used to load all the spectra, but there is no structure defined, e.g. to check and guide calibration manually.


class GBTLoad(object):
    def __init__(self, filename, src=None):
        """
        Holds a raw "unstructured" series of scans, normally not used by users
        """
        def ushow(name):
            uname = np.unique(self.sdfits.data2[:][name])
            print('uniq',name,uname)
            return uname          
        print("==GBTLoad %s" % filename)
        self.filename = filename
        self.sdfits = SDFITSLoad(filename, src)
        ushow('OBJECT')
        ushow('SCAN')
        ushow('SAMPLER')
        #ushow('PLNUM')
        #ushow('IFNUM')
        ushow('SIG')
        ushow('CAL')
        ushow('PROCSEQN')
        ushow('PROCSIZE')
        ushow('OBSMODE')  
        ushow('SIDEBAND')
        
        self.nrows = self.sdfits.nrows
        self.sp = np.empty(self.nrows, dtype=Spectrum)
        for i in range(self.nrows):
            self.sp[i] = Spectrum(self.sdfits.data2[i])
            self.sp[i].gbt['row'] = i
            
    def __len__(self):
        return self.nrows
    def __getitem__(self, index):
        return self.sp[index]
    def __repr__(self):
        return self.filename
    def stats(self, chans=None):
        """
        show Mean,RMS,Min,Max
        """
        for i in range(self.nrows):
            self.sp[i].stats(chans,label="%04d" % i)
    def debug(self, vars):
        """
        show some meta data variables
        """
        for i in range(self.nrows):
            out = ""
            for v in vars:
                out = out + repr(self.sdfits.data2[i][v]) + " "
            print(out)


# # Helper functions
# 
# * **dcmeantsys**:   calibration routine to get Tsys from calON/calOFF noise diode
# * **uniq**:         returns unique values in the order from the list (unlike np.unique)
# * **sonoff**:       helper to find the On and Off scan numbers


def dcmeantsys(calon, caloff, tcal, mode=0, fedge=10, nedge=None):
    """
    following the GBTIDL routine with same name, get the tsys from 
    the neighboring calon and caloff we define an extra way to set 
    the edge size, nedge, if you prefer to use number of edge channels
    instead of the inverse fraction
    
    calon/caloff is meant to reflect the state of the noise diode
    
    mode=0     do the mean before the division
    mode=1     do the mean after the division
    """
    nchan = len(calon)
    if nedge == None:
        nedge = nchan // fedge     # 10 %
    if mode == 0:
        meanoff = np.mean(caloff[nedge:-nedge])
        meandiff = np.mean(calon[nedge:-nedge] - caloff[nedge:-nedge])
        meanTsys = ( meanoff / meandiff * tcal + tcal/2.0 )
    else:
        meanTsys = np.mean( caloff[nedge:-nedge] / (calon[nedge:-nedge] - caloff[nedge:-nedge]) )
        meanTsys = meanTsys * tcal + tcal/2.0
    return meanTsys


def uniq(seq):
    """ from http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order """
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]


def sonoff(scan, procseqn):
    """
    return the list of On and Off scan numbers
    there must be a more elegant python way to do this....
    """
    sp = {}
    for (i,j) in zip(scan, procseqn):
        sp[i] = j
    
    us1 = uniq(scan)
    up1 = uniq(procseqn)
    
    sd = {}
    for i in up1:
        sd[i] = []
        
    for s in us1:
        sd[sp[s]].append(s)

    return sd


# # PSScan
# 
# This class holds one PS scan, which consists of an "On" and "Off" scan.
# 
# 
# The "Off" in particular can be constructed from other "Off"'s, or is a straight "Off" copy.



class PSScan(object):
    """
    Holds a PS scan - never used by users -should derive from GBTScan
    GBTLoadPS will hold one or more of such scans
    """
    #
    def __init__(self, sdfits, scan_on, scan_off):
        """
        """
        self.sdfits = sdfits
        self.status = 0
        #                           # ex1:
        self.nint = 0               # 11
        self.npol = 0               #  2
        self.on = None              # 44
        self.off = None             # 44
        self.calibrated = None      # 22
        self.timeaveraged = None    #  2
        self.polaveraged = None     #  1
        #
        self.nrows = len(scan_on)
        self.on = np.empty(self.nrows, dtype=Spectrum)
        self.off = np.empty(self.nrows, dtype=Spectrum)
        for (i,j,k) in zip(range(len(scan_on)),scan_on, scan_off):
            self.on[i] = Spectrum(sdfits.data2[j])
            self.off[i] = Spectrum(sdfits.data2[k])
            # remember the original row
            self.on[i].gbt['row'] = j
            self.off[i].gbt['row'] = k
        self.npol = 2
        self.nint = self.nrows // 4
        
    def __len__(self):
        return self.nrows
    
    def calibrate(self, verbose=False):
        """
        special PS calibration
        There are some arguments how *exactly* this is done
        """
        self.status = 1
        npolint = self.npol * self.nint
        self.calibrated = np.empty(npolint, dtype=Spectrum)
        for i in range(npolint):
            tcal = self.off[2*i].meta['TCAL']
            tcal2= self.on[2*i].meta['TCAL']
            tsys = dcmeantsys(self.off[2*i].data,  self.off[2*i+1].data,tcal)
            tsys2= dcmeantsys(self.on[2*i].data,  self.on[2*i+1].data,tcal2)
            if verbose: print(i,tcal,tsys,tsys2)
            #                 2*i is the CalON     2*i+1 the CalOFF
            #
            sig = 0.5*(self.on[2*i].data + self.on[2*i+1].data)
            ref = 0.5*(self.off[2*i].data + self.off[2*i+1].data)
            kr = self.on[2*i].gbt['row'] 
            if pjt1:
                self.calibrated[i] = Spectrum(self.on[2*i])
            else:
                self.calibrated[i] = Spectrum(self.sdfits.data2[kr])
            self.calibrated[i].data = tsys * (sig-ref) / ref
            self.calibrated[i].gbt['row'] = kr
            self.calibrated[i].gbt['tsys'] = tsys
            # fix the meta data ; most of it is ok
    def timeaverage(self):
        """
        time averaging
        """
        self.status = 2
        self.timeaveraged = np.empty(self.npol, dtype=Spectrum)
        for i in range(self.npol):
            for j in range(self.nint):
                k = i*self.nint + j
                if j == 0:
                    data = self.calibrated[k].data
                else:
                    data = data + self.calibrated[k].data
            kr = self.calibrated[k].gbt['row']   
            self.timeaveraged[i] = Spectrum(self.sdfits.data2[kr])
            self.timeaveraged[i].data = data / self.nint
            self.timeaveraged[i].gbt['row'] = kr
            # fix the meta data; most of it is ok
    def polaverage(self):
        """
        polarization averaged ; needs to be stokes smart 
        """
        self.status = 3
        self.polaveraged = np.empty(1, dtype=Spectrum)
        for i in range(self.npol):
            if i==0:
                data = self.timeaveraged[i].data
            else:
                data = data + self.timeaveraged[i].data
        kr = self.timeaveraged[0].gbt['row']
        self.polaveraged[0] = Spectrum(self.sdfits.data2[kr])
        self.polaveraged[0].data = data / self.npol
        self.polaveraged[0].gbt['row'] = kr
        # fix the meta data
        
    def finalspectrum(self):
        if self.status < 1: self.calibrate()
        if self.status < 2: self.timeaverage()
        if self.status < 3: self.polaverage()
        
        


# # ScanAvg
# 
# ScanAvg contains not only the polarization averages, but also the Stokes.
# 
# Another helper class that is normally never called by users.


class ScanAvg(object):
    """
    """
    def __init__(self):
        self.avg = None
        self.stokes = []
        


# # GBTLoadPS
# 
# This is the class that loads and calibrates Position Switched (PS) data



class GBTLoadPS(GBTLoad):
    """
    
    """
    def __init__(self, filename, src=None):
        """
        Load SDFITS into a PS structure
        - should also allow SDFITSLoad() list
        - should also allow filename list
        - all assumed hdu=1
        """
        def ushow(name, show=False):
            uname = np.unique(self.sdfits.data2[:][name])
            if show: print('uniq',name,uname)
            return uname
                              
        self.filename = filename
        self.sdfits = SDFITSLoad(filename, src)
        self.scan = {}
        self.scanaveraged = None
        self.status = 0
        #
        d = self.sdfits.data2
        self.object = ushow('OBJECT')
        self.scans = ushow('SCAN')
        pols = ushow('SAMPLER')
        sigs = ushow('SIG')
        cals = ushow('CAL')
        proc = ushow('PROCSEQN')
        ushow('PROCSIZE')
        ushow('OBSMODE',True)
        dates = ushow('DATE-OBS')
        self.date0 = dates[0]
        self.date1 = dates[-1]
        # 
        sd = sonoff(self.sdfits.data2['SCAN'], self.sdfits.data2['PROCSEQN'])    
        print('OnOff scans:',sd)
        idx = np.arange(len(self.sdfits))
        for (i1,i2) in zip(sd[1],sd[2]):
            scan_on = idx[d['SCAN'] == i1]
            scan_off = idx[d['SCAN'] == i2]
            #print(i1,'on',scan_on[0],'...',scan_on[-1])
            #print(i2,'off',scan_off[0],'...',scan_off[-1])
            self.scan[i1] = PSScan(self.sdfits, scan_on, scan_off)
        
    def summary(self):
        print("GBTLoadPS %s" % self.filename)
        print("Sources:",self.object)
        print("Scans:",self.scans)
        print("Dates:",self.date0,self.date1)
        
    def stats(self, range=None):
        print('WIP')
        
    def calibrate(self, verbose=False):
        """
        calibrate each scan
        """
        self.status = 1 
        for scan in self.scan.keys():
            print("Calibrating",scan)
            self.scan[scan].calibrate(verbose)
            
    def timeaverage(self):
        """
        average in time for each scan
        """
        self.status = 2
        for scan in self.scan.keys():
            print("Timeaver",scan)
            self.scan[scan].timeaverage()
            
    def polaverage(self):
        """
        average polarizations for each scan
        """
        self.status = 3
        for scan in self.scan.keys():
            print("Polaver",scan)
            self.scan[scan].polaverage()
            
    def scanaverage(self):
        """
        averaging over scans
        ensure there is no averaging over scans with different RA,DEC (crval2,crval3)
        """
        self.status = 4
        nscan = len(self.scan.keys())
        print("Scanaverage over %d scans" % nscan)
        self.scanaveraged = np.empty(1, dtype=Spectrum)
        for (i,scan) in zip(range(nscan),self.scan.keys()):
            kr = self.scan[scan].polaveraged[0].gbt['row']
            print('Scan %d Row %d' % (scan,kr))
            if i==0:
                data = self.scan[scan].polaveraged[0].data
            else:
                data = data + self.scan[scan].polaveraged[0].data
        self.scanaveraged[0] = Spectrum(self.sdfits.data2[kr])
        self.scanaveraged[0].data = data / nscan
        self.scanaveraged[0].gbt['row'] = kr    
        #
        if pjt1:
            sp0 = self.scan[scan].polaveraged[0]
            self.scanaveraged[0] = Spectrum(sp0)
    
    def plot(self, xrange=None, yrange=None, chans=None):
        if self.status == 3:
            for scan in self.scan.keys():
                self.scan[scan].polaveraged[0].plot(xrange,yrange,chans)
        if self.status == 4:
            self.scanaveraged[0].plot(xrange,yrange,chans)
            
    def smooth(self, win=11, method='hanning'):
        if self.status == 4:
            self.scanaveraged[0].smooth(win,method)
            
    def baseline(self, degree=2, chans=None, replace=False):
        """
        """
        if self.status == 4:
            self.scanaveraged[0].baseline(degree,chans,replace)
            
    def finalspectrum(self):
        if self.status < 1: self.calibrate()
        if self.status < 2: self.timeaverage()
        if self.status < 3: self.polaverage()
        if self.status < 4: self.scanaverage()
        print("finalspectrum is ready")
            
    def save(self, filename=None):
        print("Cannot SAVE spectra yet")
        
