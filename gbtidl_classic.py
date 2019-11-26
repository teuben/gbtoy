#
# If you import this in your ~/.ipython/profile_gbtidl/startup/50-gbt.py
# as
#      from gbtidl_classic import *
# and use a shell alias like
#
#      alias gbtidl='ipython --profile=gbtidl'
#
# it looks and feels like GBTIDL.
#

import gbtidl

#  A default GBTIDL object
g = gbtidl.GBTIDL(ndc=32)


#def filein(*args,**kwargs):
def filein(filein, verbose=False, load=True):
    """
    some help on filein here, but the real help is in g.filein()    :-(
    This is major problem 1 with this approach.
    """
    g.filein(filein,verbose,load)


