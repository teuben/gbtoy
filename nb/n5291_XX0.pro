;  this is also in the notebook embedded, but this is the code
;  that produces the ascii table, sance the commented header

filein, 'ngc5291.fits'

getps, 51, intnum=0, sampler='A9', /eqweight      ; these are 
getps, 51, plnum=1, intnum=0, /eqweight           ; equivalent

; -> Tsys:  19.30    20.08

stats,6000,12000

; -> 0.31242     0.14542 -0.28983     0.88213

write_ascii,'n5291_XX0.tab'
