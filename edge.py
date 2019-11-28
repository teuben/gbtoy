


def edge(start_scan, stop_scanx, ifnum=None, plnum=None):
    """
    Example EDGE reduction python function assuming gbtoy
    """
    scanlist = range(start_scan, stop_scan + 1)
    nscans = len(scanlist)

    g.sclear()
    if plnum == None:
        print('NOTICE: (default) will average both polarizations')
        pol = [0,1]
    else:
        pol = [plnum]

    if ifnum == None:
        print('NOTICE: (default) IFNUM=1')
        ifnum=1

    for i in range(nscans):
        # info = scan_info(scanlist[i])
        j = i%3 - 1      # j==0 is always the ref, on either side are the sig's
        if j == 0:  continue
        for p in pol:
            g.getsigref(scanlist[i],scanlist[i-j],ifnum=ifnum,plnum=p)
            g.accum()
    g.ave()
    g.show()
