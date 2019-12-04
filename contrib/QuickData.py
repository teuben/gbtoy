#!/usr/bin/env python
###############################################################################
#                                                                             #
# NAME:    QuickData.py                                                       #
#                                                                             #
# PURPOSE: Quick and dirty GUI to reduce position-switched data from mops.    #
#                                                                             #
# UPDATED: 10 Mar 2009 by cpurcell                                            #
#                                                                             #
###############################################################################

# Import the necessary modules.
import copy,  os, sys, re, string, math, time, copy, shutil
from Tkinter import *
from tkFileDialog import askopenfilenames
from asap import *

# Some default settings
# Causes errors with the current development version (ASAP 2.3 pre-release)
#plotter.set_histogram()

#=============================================================================#
# Class defining the main graphical interface                                 #
#=============================================================================#
class mainGUI:
   
   def __init__(self, master):

      # Set the default save format
      self.save_format="FITS"

      # Create the master frame
      mainFrame = Frame(master, relief='flat', borderwidth=2)
      mainFrame.grid(sticky = W+E+N+S)
      master.title('Quick Data')
      master.rowconfigure(0, weight = 1 )
      master.columnconfigure( 0, weight =1 )

#--------------------------- Loading Frame -----------------------------------#
      loadFrame = Frame(mainFrame, relief='solid', borderwidth=2)

      # Create and draw the Dir entry box
      self.lDir = Label(loadFrame,text="Dir:")
      self.lDir.grid(row=0, column=0, columnspan=1, sticky=W+N+S )
      self.eDir = Entry(loadFrame,bg="white")
      self.eDir.grid(row=0, column=1, columnspan=7, sticky = W+E+N+S )
      
      # Create and draw the File entry box
      self.lFile = Label(loadFrame,text="Files:")
      self.lFile.grid(row=1, column=0, columnspan=1, sticky=W+N+S )
      self.eFile = Entry(loadFrame,bg="white")
      self.eFile.grid(row=1, column=1, columnspan=7, sticky = W+E+N+S )

      # Create and draw the settings, browse, load and quit button
      self.bSettings = Button(loadFrame, text="Settings", height=1, width=6, \
                          command=self.settingsEvent)
      self.bSettings.grid(row=3, column=0, columnspan=2, sticky=W+E )
      self.bBrowse = Button(loadFrame, text="Browse", height=1, width=6, \
                          command=self.browseEvent)
      self.bBrowse.grid(row=3, column=2, columnspan=2, sticky=W+E )
      self.bLoad = Button(loadFrame, text="Load", height=1, width=6, \
                          command=self.loadEvent)
      self.bLoad.grid(row=3, column=4, columnspan=2, sticky=W+E )
      self.bQuit = Button(loadFrame, text="Quit", height=1, width=6, \
                          command=self.exit_clean)
      self.bQuit.grid(row=3, column=6, columnspan=2, sticky=W+E)
      
      loadFrame.grid(row=0, column=0, sticky = W+E+N )

#-------------------------- IF selection frame -------------------------------#
      ifselFrame = Frame(mainFrame, relief='solid', borderwidth=2)
      
      # Create and draw the IF menu button
      self.ifLabel = Label(ifselFrame, text="Current IF: ")
      self.ifLabel.grid(row=0, column=0, columnspan=2, sticky=W)
      self.ifMenu = Menubutton(ifselFrame, text="--", relief='raised')
      self.ifMenu.grid(row=0, column=2, sticky=W)
      self.ifMenu.menu = Menu(self.ifMenu, tearoff=0)
      self.ifMenu["menu"] = self.ifMenu.menu

      # Create and draw the input scan list boxes
      self.in0ScrollBar = Scrollbar(ifselFrame, orient=VERTICAL)
      self.pol0ScanList = Listbox(ifselFrame, selectmode=MULTIPLE, \
                                  exportselection=NO, bg='blue', fg='yellow', \
                                  yscrollcommand=self.in0ScrollBar.set,
                                  width=9, height=4)
      self.in0ScrollBar.config(command=self.pol0ScanList.yview)
      
      self.in1ScrollBar = Scrollbar(ifselFrame, orient=VERTICAL)
      self.pol1ScanList = Listbox(ifselFrame, selectmode=MULTIPLE, \
                                  exportselection=NO, bg='blue', fg='yellow', \
                                  yscrollcommand=self.in1ScrollBar.set,
                                  width=9, height=4)
      self.in1ScrollBar.config(command=self.pol1ScanList.yview)
      
      self.pol0ScanList.grid(row=1, column=0, columnspan=2, sticky=W+E+N+S )
      self.in0ScrollBar.grid(row=1, column=2, sticky=W+N+S )
      self.pol1ScanList.grid(row=1, column=3, columnspan=2, sticky=W+E+N+S)
      self.in1ScrollBar.grid(row=1, column=5, sticky=W+N+S )

      # Create and draw the average buttons
      self.avg0Button = Button(ifselFrame, text="Avg Time", 
                               width=5, height=1, command=lambda
                               arg1=0 : self.avgTimeCmd(arg1))
      self.avg1Button = Button(ifselFrame, text="Avg Time", 
                               width=5, height=1, command=lambda
                               arg1=1 : self.avgTimeCmd(arg1))
      self.avg0Button.grid(row=2, column=0,columnspan=2, sticky=W+E+N+S )
      self.avg1Button.grid(row=2, column=3,columnspan=2, sticky=W+E+N+S )
      
      # Create and draw the output scan list box
      self.out0ScanList = Listbox(ifselFrame, selectmode=SINGLE, \
                                  exportselection=NO, bg='green', fg='black', \
                                  width=9, height=1)
      self.out1ScanList = Listbox(ifselFrame, selectmode=SINGLE, \
                                  exportselection=NO, bg='green', fg='black', \
                                  width=9, height=1)
      self.out0ScanList.grid(row=3, column=0, columnspan=2, sticky=W+E+N+S )
      self.out1ScanList.grid(row=3, column=3, columnspan=2, sticky=W+E+N+S )

      # Ceate and draw the avg_pol button & scan list
      self.avgPButton = Button(ifselFrame, text="Avg Polarisations", 
                               width=9, height=1, command=self.avgPolCmd)
      self.avgPButton.grid(row=4, column=0, columnspan=4, sticky=W+E+N+S )

      # Create and draw the output scan list box
      self.outPScanList = Listbox(ifselFrame, selectmode=SINGLE, \
                                  exportselection=NO, bg='yellow', fg='black',\
                                  height=1)
      self.outPScanList.grid(row=5, column=0, columnspan=4, sticky=W+E+N+S)
      
      ifselFrame.grid(row=0, column=1, rowspan=6, sticky = W )
      
#----------------------- Save current spectrum frame -------------------------#
      saveFrame = Frame(mainFrame, relief='solid', borderwidth=2)

      # Create and draw the save button
      self.saveLabel = Label(saveFrame, text="Save Format:")
      self.saveLabel.grid(row=0, column=0,columnspan=2, sticky=W)
      self.saveMenu = Menubutton(saveFrame, text="--", relief='raised', width=10)
      self.saveMenu.grid(row=0, column=2, columnspan=2,sticky=W)
      self.saveMenu.menu = Menu(self.saveMenu, tearoff=0)
      self.saveMenu["menu"] = self.saveMenu.menu
      self.initSave()
      self.saveButton = Button(saveFrame, text="Save", 
                               width=8, height=1, command=lambda
                               arg1=self.save_format :
                               self.saveScan(arg1))
      self.saveButton.grid(row=12, column=0, columnspan=6, sticky=W+E+N+S)
      
      saveFrame.grid(row=0, column=3, rowspan=3, sticky = W+E+N )
      
#-----------------------------------------------------------------------------#

      # Select event bindings in listboxes
      self.pol0ScanList.bind('<ButtonRelease-1>', lambda event,
                             arg1=self.pol0ScanList,
                             arg2='raw',
                             arg3=0 : 
                             self.selectScanEvent(event,arg1,arg2,arg3))
      self.pol1ScanList.bind('<ButtonRelease-1>', lambda event,
                             arg1=self.pol1ScanList,
                             arg2='raw',
                             arg3=1 : 
                             self.selectScanEvent(event,arg1,arg2,arg3))
      self.out0ScanList.bind('<ButtonRelease-1>', lambda event,
                             arg1=self.out0ScanList,
                             arg2='avgt',
                             arg3=0 : 
                             self.selectScanEvent(event,arg1,arg2,arg3))
      self.out1ScanList.bind('<ButtonRelease-1>', lambda event,
                             arg1=self.out1ScanList,
                             arg2='avgt',
                             arg3=1 : 
                             self.selectScanEvent(event,arg1,arg2,arg3))
      self.outPScanList.bind('<ButtonRelease-1>', lambda event,
                             arg1=self.outPScanList,
                             arg2='avgp',
                             arg3=0 : 
                             self.selectScanEvent(event,arg1,arg2,arg3))

#================== Event/command handling code below here ===================#

   # Open the settings dialog box
   def settingsEvent(self):
      settingsDialogue = settingsGUI(root)
      
   # Open a file browser 
   def browseEvent(self):
      
      self.eDir.delete(0,END)
      self.eFile.delete(0,END)
      path_tup=askopenfilenames(filetypes=[("allfiles","*")])
      folder=''; files=[]
      for entry in path_tup:
         (folder,file) = os.path.split(entry)
         files.append(file)
      self.eDir.insert(0,folder)
      self.eFile.insert(0,(','.join(files)))
      
   # Events bound to the LOAD button
   def loadEvent(self):

      # Create an instance of the dataManager Class and load the file(s)
      self.data_mgr = dataManager()
      files=self.eFile.get().split(',')
      directory = self.eDir.get().rstrip('/')
      self.data_mgr.loadData(files, directory)

      # Run the init method to load the scans from IF=0 into the ListBoxes
      self.initIF(IF=0)
      
   # Initialise the input and averaged list boxes with the scan numbers
   # NB: Currently assumes two polarisations!
   def initIF(self, IF=0):
      self.data_mgr.current_IF=IF

      # Add the scan list to the raw scans list boxes
      self.scans2listbox(self.data_mgr.if_scantabs[IF][0],self.pol0ScanList)
      self.scans2listbox(self.data_mgr.if_scantabs[IF][1],self.pol1ScanList)
      
      # Add saved time-averaged scans to the time-averaged list boxes
      self.scans2listbox(self.data_mgr.avgt_scantabs[IF][0],self.out0ScanList)
      self.scans2listbox(self.data_mgr.avgt_scantabs[IF][1],self.out1ScanList)

      # Add the scan list to the polarisation averaged box
      self.scans2listbox(self.data_mgr.avgp_scantabs[IF][0],self.outPScanList)
      
      # Add the choice of IFs to the IF selector MenuBox
      self.ifMenu.menu.delete(0,END)
      for i in range(len(self.data_mgr.if_scantabs)):
         self.ifMenu.menu.add_command(label="IF %s" % i, command=lambda
                                      arg1=i : self.initIF(IF=arg1))
      self.ifMenu.configure(text="IF %s" % IF)

      # Plot the first scan of the first IF/POL
      scn1 = self.data_mgr.if_scantabs[0][0].getscannos()[0]
      self.data_mgr.plot_scan(scan_no=scn1,IF=0,POL=0,target='raw')
      del scn1
      
   # Load the scan-numbers from a scantable into a listbox
   def scans2listbox(self,scantable,listbox):
      listbox.delete(0,END)
      try:
         scannos = scantable.getscannos()
         for scan in scannos:
            listbox.insert(END,scan)
      except Exception:
         print ""

   # Initialise the save format menu
   def initSave(self,format='FITS'):
      self.saveMenu.menu.delete(0,END)
      self.saveMenu.menu.add_command(label="FITS", command=lambda
                                     arg1='FITS' :
                                     self.initSave(arg1))
      self.saveMenu.menu.add_command(label="ASCII", command=lambda
                                     arg1='ASCII' :
                                     self.initSave(arg1))
      self.saveMenu.menu.add_command(label="SDFITS", command=lambda
                                     arg1='SDFITS' :
                                     self.initSave(arg1))
      self.saveMenu.configure(text=format)
      self.save_format=format

   # Exit the program and clean up temporary files
   def exit_clean(self):
      tempfile_list = lst_dir(regexp='^temp\d+_\d+$')
      print "Deleting %s temporary files ..." % len(tempfile_list),
      for tempfile in tempfile_list:
         if os.path.exists(tempfile): shutil.rmtree(tempfile,True)
      print "done."
      os.sys.exit(0)         

#-----------------------------------------------------------------------------#

   # Events bound to a SELECT mouse-up event on the listboxes
   # Determine the scan number and plot that scan
   def selectScanEvent(self,event,listbox,target,POL):
      IF=self.data_mgr.current_IF
      if target=='avgt': scantab=self.data_mgr.avgt_scantabs
      elif target=='avgp': scantab=self.data_mgr.avgp_scantabs
      else: scantab=self.data_mgr.if_scantabs
      index = int(listbox.nearest(event.y))
      try:
         selected = scantab[IF][POL].getscannos()[index]
         self.data_mgr.plot_scan(IF=IF,scan_no=selected,POL=POL,target=target)
      except Exception:
         print "Failed to select & plot scantable (does not exist yet?)."
      del index
      
   # Command bound to the Average_Time Buttons
   def avgTimeCmd(self,POL):
      IF=self.data_mgr.current_IF
      if POL==0: 
         inlistbox=self.pol0ScanList
         outlistbox=self.out0ScanList
      else: 
         inlistbox=self.pol1ScanList
         outlistbox=self.out1ScanList
      index_list=inlistbox.curselection()
      scans=[]
      for index in index_list: scans.append(int(inlistbox.get(index)))
      self.data_mgr.avg_time(POL,scans)
      self.scans2listbox(self.data_mgr.avgt_scantabs[IF][POL],outlistbox)

   # Average the polarisations of the time averaged scans
   def avgPolCmd(self,IF=None):
      IF=self.data_mgr.current_IF
      self.data_mgr.avg_pol(IF=IF)
      self.scans2listbox(self.data_mgr.avgp_scantabs[IF][0],self.outPScanList)

   # Save a scan
   def saveScan(self, format):
      print "Saving current scan in format '%s'" % self.save_format
      IF=self.data_mgr.current_IF
      scan_no=self.data_mgr.current_scan
      POL=self.data_mgr.current_pol
      target=self.data_mgr.target      
      if target=='avgt': s=self.data_mgr.avgt_scantabs[IF][POL]
      elif target=='avgp': POL=0; s=self.data_mgr.avgp_scantabs[IF][POL]
      else: s=self.data_mgr.if_scantabs[IF][POL]

      print "SAVING: IF=%s POL=%s SCAN=%s" % (IF, POL, scan_no),
      print "TARGET=%s" % target      
      sel1 = selector()
      sel1.set_ifs(IF)
      sel1.set_polarisations(POL)
      sel1.set_scans(scan_no)
      s.set_selection(sel1)
      name=s.get_sourcename()[0]+'_'
      s.save(name,format=self.save_format,overwrite=True)
      s.set_selection()
      del sel1, s


#=============================================================================#
# The settings dialogue box                                                   #
#=============================================================================#
class settingsGUI:
   def __init__(self, parent):
      top = self.top = Toplevel(parent)
      Label(top, text="Pre-processing:").pack()

      self.e = Entry(top)
      self.e.insert(0,"Not implemented yet.")
      self.e.pack(padx=5)

      b = Button(top, text="OK", command=top.destroy)
      b.pack(pady=5)

   
#=============================================================================#
# Data manager object - keep track of the loaded scans                        #
#=============================================================================#
class dataManager:
   def __init__(self):

      # Track the last accessed scan table/IF/polarisation/scan
      self.if_scantabs=[]
      self.avgt_scantabs=[]
      self.avgp_scantabs=[]
      self.current_IF=0
      self.current_scan=0
      self.current_pol=0
      self.current_target='raw'
      
   # Load and quotient the data, merging multiple scantables if necessary
   def loadData(self,files, directory=".",doppler='RADIO',freqframe='LSRK'):

      # Load and quotient each file in turn
      sourcename_dict={}
      quot_scantabs=[]
      merged_scantabs=None
      for file in files:
         load_file = directory + "/" + file
         s = scantable(load_file, average=True)
         q = s.auto_quotient(preserve=False)
         sourcename_dict[q.get_sourcename()[0]] = 1
         q.set_doppler(doppler)
         q.set_freqframe(freqframe)
         quot_scantabs.append(q)
         del s, q

      # Check all files contain the same named source
      if len(sourcename_dict)>1:
         print "Selected files contain more than one source:"
         print sourcename_dict.keys()
         sys.exit(0)
         
      # If more than one file loaded, then merge the scantables
      if len(quot_scantabs) > 1:
         merged_scantabs=(merge(quot_scantabs))
      else:
         merged_scantabs=(quot_scantabs[0].copy())
      del quot_scantabs

      # Slice the merged scantable by IF & POL
      print "Slicing input scantable by IF and Polarisation:"
      for i in range(merged_scantabs.nif()):
         templst=[]
         for j in range(merged_scantabs.npol()):
            print "IF: %s, POL: %s" % (i,j)
            sel1=selector()
            sel1.set_ifs(i)
            sel1.set_polarisations(j)
            merged_scantabs.set_selection(sel1)
            templst.append(merged_scantabs.copy())
         self.if_scantabs.append(templst)
         del templst, j

      # Create an empty nested array to hold the results of the 
      # time-averaging operation
      for i in range(merged_scantabs.nif()):
         templst=[]
         for j in range(merged_scantabs.npol()):
            templst.append(None)
         self.avgt_scantabs.append(templst)
         del templst, j

      # Create an empty nested array to hold the results of the 
      # polarisation-averaging operation
      for i in range(merged_scantabs.nif()):
         self.avgp_scantabs.append([None])
      del merged_scantabs, i

   # Return some information about the raw or averaged scantables
   def getScantabInfo(self,IF=0, POL=0, target='raw'):
      if target=='avgt': s=self.avgt_scantabs
      elif target=='avgp': s=self.avgp_scantabs
      else:  s=self.if_scantabs
      try:
         scannos = s[IF][POL].getscannos()
         sourcename= s[IF][POL].get_sourcename()
         tsys= s[IF][POL].get_tsys()
         elevation= s[IF][POL].get_elevation()
         del s

         # Index the information via a dictionary
         scan_info=[]
         for i in range(len(scannos)):
            info={}
            info['sourcename'] = sourcename[i]
            info['tsys'] = tsys[i]
            info['scan'] = scannos[i]
            scan_info.append(info)
         return scan_info
      except Exception:
         return []

   # Plot a scan 
   def plot_scan (self, scan_no=0, IF=0, POL=0, target='raw'):
      if not IF: IF=self.current_IF
      if target=='avgt': s=self.avgt_scantabs[IF][POL]
      elif target=='avgp': POL=0; s=self.avgp_scantabs[IF][POL]
      else: s=self.if_scantabs[IF][POL]
      self.current_IF = IF
      self.current_pol = POL
      self.current_scan =scan_no
      self.target = target
      print "PLOTTING: IF=%s POL=%s SCAN=%s" % (IF, POL, scan_no),
      print "TARGET=%s" % target      
      sel1 = selector()
      sel1.set_ifs(IF)
      sel1.set_polarisations(POL)
      sel1.set_scans(scan_no)
      s.set_selection(sel1)
      s.set_unit('GHz')
      plotter.plot(s)
      s.set_unit('channel')
      s.set_selection()
      del sel1, s
      
   # Average the selected scans in time.
   def avg_time(self,POL=0, scans=[]):
      IF=self.current_IF
      s = self.if_scantabs[IF][POL]
      sel1=selector()
      sel1.set_scans(scans)
      s.set_selection(sel1)
      self.avgt_scantabs[IF][POL] = s.average_time(weight='tintsys',align=True)
      self.plot_scan(scan_no=0,IF=IF,POL=POL,target='avgt')
      s.set_selection()
      del sel1, s

   # Average the selected polarisations together
   def avg_pol(self,IF=None):
      IF=self.current_IF
      pol0=self.avgt_scantabs[IF][0].copy()
      pol1=self.avgt_scantabs[IF][1].copy()
      mrg=merge(pol0,pol1)
      del pol0, pol1
      mrg1=mrg.average_pol()
      del mrg
      self.avgp_scantabs[IF][0] = mrg1.average_time()
      del mrg1
      self.plot_scan(scan_no=0,IF=IF,POL=0,target='avgp')


#=============================================================================#
# List the files in the current directory, filter according to a regexp       #
#=============================================================================#
def lst_dir(regexp='^.*\..*$'):
    dirlist=os.listdir('.')
    pattern = re.compile(regexp)
    outlist=[]
    for file_name in dirlist:
        if pattern.match(file_name):
            outlist.append(file_name)
    return outlist

 
#=============================================================================#
# Message deliniated by a line of '-' characters                              #
#=============================================================================#
def message (string):
    print "\n"+"-"*80
    print "> %s" % string
    print "-"*80


#==================== Initialise the GUI and event loop ======================#
root = Tk()
app = mainGUI(root)
root.mainloop()
