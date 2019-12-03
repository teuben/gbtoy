# gbtoy

Toying with gbt spectra in python. This repo can also install it's own python (anaconda3) if you
to shield yourself from a system version. You can also try making your own virtual conda environment
using the system conda. See Makefile for targets.


## notes

* gbtidl does not work with gdl, it really needs IDL; pydl also does not seem useful

* Lots of info on http://gbtidl.nrao.edu/

* ARGUS specific things on http://www.gb.nrao.edu/argus/

* Example data  and commands for gbtidl on http://www.gb.nrao.edu/GBT/DA/gbtidl/users_guide/node72.html

* The [sdfits](https://fits.gsfc.nasa.gov/registry/sdfits.html) convention webpage has an example TREG_091209.cal.acs.fits SDFITS file that appears to have correct headers, the other one, PParkes_GASS.fits , has something missing

* https://github.com/pyspeckit     pyspeckit  (has routines to read GBT/SDFITS data; Adam Ginsburg))

* https://github.com/astropy/specutils  astropy's workflow.

* https://github.com/spacetelescope/specviz  specviz

* specreduce

* https://github.com/astropy/astropy-APEs/blob/master/APE13.rst Vision for Astropy Spectroscopic Tools

* https://github.com/radio-astro-tools/   varoious modules (spectral-cube, radio-beam,gaussfit_catalog , signal-id) 

* https://github.com/GreenBankObservatory   gbt-pipeline and gbtgridder

* https://github.com/GBTSpectroscopy  gbtpipe (Erik Rosolowsky)

* https://sourceforge.net/p/aoflagger/wiki/Home/ aoflagger

* http://www.mrao.cam.ac.uk/~rachael/specx/ SpecX - part of starlink (JCMT, 2002)
