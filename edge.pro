; edge data reduction script for GBTIDL
;
; formerly called reduce_15b287.pro by Tony Wong

pro edge, start_scan,stop_scan, ifnum=ifnum, plnum=plnum

  npar = n_params()
  if npar EQ 1 then begin
     scanlist = start_scan
  endif else begin
     if npar EQ 2 then begin
        if stop_scan GT start_scan then begin
           scanlist = lindgen(stop_scan-start_scan+1)+start_scan
        endif else begin
           print,'ERROR: start_scan > stop_scan'
           return
        endelse
     endif else begin
        print,'ERROR: Incorrect number of input parameters'
        return
     endelse
  endelse
  nscans = n_elements(scanlist)

  sclear
  if n_elements(plnum) EQ 0 then begin
     print,'NOTICE: (default) will average both polarizations'
     both_pol = 1
     pol1 = 0
     pol2 = 1
  endif else begin
     both_pol = 0
     pol1 = plnum
  endelse
  if n_elements(ifnum) EQ 0 then begin
     print,'NOTICE: (default) IFNUM=1'
     ifnum=1
  endif

  for i = 0, nscans-1 do begin
     info = scan_info(scanlist[i])
     if size(info,/type) NE 8 then begin
        print,'WARNING: Scan '+strcompress(string(scanlist[i]),/remove_all)+$
              ' is not valid'
        goto,next_scan
     endif
     scnstr = strcompress(string(scanlist[i]),/remove_all)
     pol1str = info.polarizations[info.plnums[pol1]]
     if i mod 3 EQ 0 and i LT nscans then begin
        print,'On: '+scnstr+$
              '  Off: '+strcompress(string(scanlist[i+1]),/remove_all)+$
              '  Pol: '+pol1str
        getsigref,scanlist[i],scanlist[i+1],ifnum=ifnum,plnum=pol1
        accum
     endif
     if i mod 3 EQ 2 then begin
        print,'On: '+scnstr+$
              '  Off: '+strcompress(string(scanlist[i-1]),/remove_all)+$
              '  Pol: '+pol1str
        getsigref,scanlist[i],scanlist[i-1],ifnum=ifnum,plnum=pol1
        accum
     endif
     if both_pol EQ 1 then begin
        pol2str = info.polarizations[info.plnums[pol2]]
        if i mod 3 EQ 0 and i LT nscans then begin
           print,'On: '+scnstr+$
                 '  Off: '+strcompress(string(scanlist[i+1]),/remove_all)+$
                 '  Pol: '+pol2str
           getsigref,scanlist[i],scanlist[i+1],ifnum=ifnum,plnum=pol2
           accum
        endif
        if i mod 3 EQ 2 then begin
           print,'On: '+scnstr+$
                 '  Off: '+strcompress(string(scanlist[i-1]),/remove_all)+$
                 '  Pol: '+pol2str
           getsigref,scanlist[i],scanlist[i-1],ifnum=ifnum,plnum=pol2
           accum
        endif
     endif
     next_scan:
  endfor
  ave
  print,'On-source time (not total time): '+$
        strcompress(string(!g.s[0].exposure),/remove_all)+$
        ' sec = ' + $
        strcompress(string(!g.s[0].exposure/60.0),/remove_all)+$
        ' min'
        
  !g.s[0].line_rest_frequency=1.42040575d9
  show

end

; 1.42040575
; 1.420405751786
; c=299792.458000
