#

gbtoy.pdf:   gbtoy.tex gbtoy.bib
	pdflatex gbtoy
	bibtex  gbtoy
	pdflatex gbtoy
	pdflatex gbtoy

#      bring (ana)conda up to date, assuming you have write permission
conda:
	@echo Using `which conda` to update your conda
	conda update conda

#      optionally install our own anaconda3 as your python
#      be sure to source the python_start.sh script after this
python:
	./install_anaconda3

git:  specutils pyspeckit spectral-cube gbt-pipeline gbtgridder gbtpipe

specutils:
	git clone https://github.com/astropy/specutils

specreduce:
	git clone https://github.com/astropy/specreduce

pyspeckit:
	git clone https://github.com/pyspeckit/pyspeckit

pyspeckit2:
	git clone https://github.com/teuben/pyspeckit
	(cd pyspeckit; git checkout teuben-gbt)

specviz:
	git clone https://github.com/spacetelescope/specviz

spectral-cube:
	git clone https://github.com/radio-astro-tools/spectral-cube

statcont:
	git clone https://github.com/radio-astro-tools/statcont

gbt-pipeline:
	git clone https://github.com/GreenBankObservatory/gbt-pipeline

gbt-pipeline2:
	git clone https://github.com/teuben/gbt-pipeline
	(cd gbt-pipeline; git checkout python3)

gbtgridder:
	git clone https://github.com/GreenBankObservatory/gbtgridder

gbtpipe:
	git clone https://github.com/GBTSpectroscopy/gbtpipe

comb:
	git clone https://github.com/mpound/comb
