# Example gbtoy python version of edge.pro
# Formerly called reduce_15b287.pro by Tony Wong

def edge(start_scan, stop_scan, ifnum=1, plnum=[0,1]):
    """  for total power tracks for EDGE survey
    """
    scanlist = g.range(start_scan, stop_scan)
    nscans = len(scanlist)

    g.sclear()

    for i in range(nscans):
        # info = scan_info(scanlist[i])
        j = i%3 - 1      # j==0 is always the ref, on either side are the sig's
        if j == 0:  continue
        for pol in plnum:
            print(scanlist[i],scanlist[i-j])
            g.getsigref(scanlist[i],scanlist[i-j],ifnum=ifnum,plnum=pol)
            g.accum()
    g.ave()
    g.show()
