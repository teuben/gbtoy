from asap import *

# Define the file name
file='2008-03-12_0932-M999.rpf'

# Load the file into memory
s = scantable(file, average=True)
print s

# Set the plotting mode
plotter.set_mode(stacking='i', panelling='t')

# Set the doppler convention
s.set_doppler('RADIO')

# Set the rest fram
s.set_freqframe('LSRK')

# Set the observed rest frequency in MHz
s.set_restfreqs([86243.37e6])

# Define the channel unit
s.set_unit('km/s') 

# Form the quotient spectra
q=s.auto_quotient()

plotter.plot(q)

print "Press <Return> to continue ..."
raw_input()

# Average all scans in time, aligning in velocity
av = q.average_time(align=True)

# Remove the baseline (set to 0)
msk = av.create_mask([-200,-50],[50,180])
av.poly_baseline(msk,0)

# Average the two polarisations together
iav = av.average_pol()

# Smooth the data with boxcar, full width = 3
siav = iav.smooth(kernel = 'boxcar', width = 3, insitu = False)
plotter.plot(siav)


# Scale the data according to scaling fudge factor
#iav.scale(2)  #With beam efficiency of 0.49 at 86 GHz

# Make final plot for saving
plotter.set_range(-20,30)  
plotter.plot(siav)
plotter.set_legend(mode=-1)
plotter.set_title(['Orion-SiO'], fontsize=18) 
plotter.text(10,95,"SiO (2-1 v=1) at 86243.440 MHz", fontsize=12)
plotter.text(-19,95,"2008/03/12", fontsize=12)
plotter.text(-19,90,"Zoom Mode", fontsize=12)
#save plot
plotter.save('Orion-SiO.ps')


