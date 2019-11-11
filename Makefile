#




gbtoy.pdf:   gbtoy.tex gbtoy.bib
	pdflatex gbtoy
	bibtex  gbtoy
	pdflatex gbtoy
	pdflatex gbtoy

git:  specutils pyspeckit spectral-cube gbt-pipeline gbtgridder gbtpipe

specutils:
	git clone https://github.com/astropy/specutils

pyspeckit:
	git clone https://github.com/pyspeckit/pyspeckit

pyspeckit2:
	git clone https://github.com/teuben/pyspeckit
	(cd pyspeckit; git checkout teuben-gbt)

spectral-cube:
	git clone https://github.com/radio-astro-tools/spectral-cube

gbt-pipeline:
	git clone https://github.com/GreenBankObservatory/gbt-pipeline

gbtgridder:
	git clone https://github.com/GreenBankObservatory/gbtgridder

gbtpipe:
	git clone https://github.com/GBTSpectroscopy/gbtpipe
