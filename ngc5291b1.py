#! /usr/bin/env python
#
#

import numpy as np
# import matplotlib
from matplotlib import pyplot as plt

import gbt1 as gbt

xrange=[3000,5500]
yrange=[-0.05,0.55]

plt.figure()

ps = gbt.GBTLoadPS('ngc5291.fits')     # load the SDFITS file
ps.summary()                           # overview times, sources, scans etc.
ps.finalspectrum()                     # calibrate and time/pol/scan average
ps.plot(xrange=xrange, yrange=yrange)  # review the final plot 
ps.smooth(win=51)                      # smooth with a 51 window
ps.baseline
ps.baseline(chans=[(3500,14000),(19000,30000)])
ps.plot(xrange=xrange, yrange=yrange)  # (over)plot
ps.baseline(chans=[(3500,14000),(19000,30000)],replace=True)
ps.plot(xrange=xrange, yrange=yrange)  #(over)plot
ps.save('a1.fits')                     # save the spectrum (also SDFITS format)

plt.show()
