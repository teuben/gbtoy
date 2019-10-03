#    -*- python -*-
#
#
#  GBTIDL - emulator of some examples implemented in python
#
#  GBTOY is the kiddy version
#  GBTPY is when it's really python?
# 
#  this needs a hacked version of pyspeckit.py  (the "teuben-gbt1" branch)
#
#
#  !gc.xxx   ->   g.gc.xxx
#  !g.s[0]   ->   g.s[0]

import numpy as np


# helper class for the !gc constants 

class GC(object):
    def __init__(self):
        print("GC")
        self.light_speed = np.double(2.99792458e8)   # m/s
        self.light_c     = np.double(2.99792458e5)   # km/s

# helper class for the DC's

class DataContainer(object):
    """ Emulate IDL's DataContainer (DC) and how GBTIDL is using them
    """
    def __init__(self):
        self.o = None

    def set(self, o):
        self.o = o
        
# the main class:  the g object is what the user needs to instantiate

class GBTIDL(object):
    """
    GBTIDL emulator. This class simply holds a lot of the global parameters
    and provides setters and getters

    g = gbtidl.GBTIDL() 
    g.s[0]    is the PDC for spectra
    g.c[0]    is the PDC for continuum
   
    
    """
    def __init__(self, filein=None, dirin=None, ndc=16):
        self.filein = None     # optional SDFITS file
        self.dirin  = None     # optional directory with related SDFITS files
        self.mode   = 0        # none (0) or file (1) or dir (2)
        self.s      = list(range(ndc))
        self.c      = list(range(ndc))
        for i in range(ndc):
            self.s[i] = DataContainer()
            self.c[i] = DataContainer()
        self.gc = GC()
        

        self.help()

    def help(self, concept=None):
        
        _help = """
        --------------------------------------------------------------------
                    Welcome to GBTOY v0.0.1
        
                   http://github.edu/teuben/gbtoy

        For help with a GBTOY routine from the command line, use
             the procedure 'usage'.  For example:

        usage('show')          ; gives the syntax of the procedure 'show'
        usage('show',True)     ; gives more information on 'show'
        --------------------------------------------------------------------
        """
        print(_help)
        

    def filein(self, filein=None):
        """ if no filein given, should pop up filebrowser
        """
        print("GBTIDL> ")

    def dirin(self, dirin=None):
        """ if no dirin given, should pop up filebrowser
        """
        print("GBTIDL> ")
        
    def summary(self, logfile=None):
        print("GBTIDL> ")
        """
        Scan Source  Vel  Proc Seq  RestF nIF nInt nFd  Az  El
        -------------------------------------------------------------------------------
        79  W3OH  -44.0  Track 0 1.667 2 6 1 379.2 16.1
        80  W3OH  -44.0  Track 0 1.667 2 6 1 379.4 16.2
        """

    def header(self, buffer=0):
        print("GBTIDL> ")
        
    def list(self, start=0, end=10):
        """ start=0 is the first
        """
        print("GBTIDL> ")

    def files(self):
        print("GBTIDL> ")

    def getfs(self, scan=None):
        print("GBTIDL> ")

    def getps(self, scan=None):
        print("GBTIDL> ")

    def getrec(self, record=None):
        print("GBTIDL> ")

    def getdata(self):
        print("GBTIDL> ")

    def setdata(self, data):
        print("GBTIDL> ")

    def setregion(self, region=[]):
        print("GBTIDL> ")

    def nfit(self, order=0):
        print("GBTIDL> ")

    def baseline(self):
        print("GBTIDL> ")

    def fitgauss(self):
        print("GBTIDL> ")

    def print_ps(self):
        print("GBTIDL> ")
        
    def print_png(self):
        print("GBTIDL> ")
        
    def print_pdf(self):
        print("GBTIDL> ")
        
    def fileout(self, fileout):
        print("GBTIDL> ")

    def keep(self):
        print("GBTIDL> ")
        
    def exit(self):
        print("GBTIDL> ")

    def online(self):
        print("GBTIDL> ")
        
    def offline(self):
        print("GBTIDL> ")
        
    def copy(self, r1, r2):
        print("GBTIDL> ")

    def add(self, r1, r2, rsum):
        print("GBTIDL> ")

    def show(self, r):
        print("GBTIDL> ")

    def bshape(self, modelbuffer):
        print("GBTIDL> ")
        
    def subtract(self, r1, r2, rsub):
        print("GBTIDL> ")

    def usage(self, task, verbose=False):
        """ print the long or short __docstring__
        """

# example from manual how IDL and OY compare
def myscale(g, factor=1.0):
    """
    pro myscale,factor
      tmp_data = getdata()
      tmp_data = tmp_data * factor
      setdata, tmp_data
      if !g.frozen eq 0 then show
    end
    """
    g.setdata(factor * g.getdata())
    # if !g.frozen eq 0 then show

