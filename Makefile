#

# this is the new way
gbtoy:
	git clone https://git.overleaf.com/5ddecdf65bbba7000140ea5f gbtoy

pdf:  gbtoy.pdf 


# this is old
gbtoy.pdf:   gbtoy.tex gbtoy.bib
	pdflatex gbtoy
	bibtex  gbtoy
	pdflatex gbtoy
	pdflatex gbtoy

#      bring (ana)conda up to date, assuming you have write permission
conda:
	@echo Using `which conda` to update your conda
	conda update conda

#      this has not been tested 
conda_test:
	conda update conda
	conda env create -f environment.yml
	conda activate gbtoy1
	python -m ipykernel install --user --name gbtoy1 --display-name "gbtoy1"
	jupyter notebook


#      optionally install our own anaconda3 as your python
#      be sure to source the python_start.sh script after this
python:
	./install_anaconda3

git:  specutils pyspeckit spectral-cube gbt-pipeline gbtgridder gbtpipe

specutils:
	git clone https://github.com/astropy/specutils

specreduce:
	git clone https://github.com/astropy/specreduce

pyspeckit-tests:
	git clone https://github.com/pyspeckit/pyspeckit-tests

# my development
pyspeckit:
	git clone https://github.com/teuben/pyspeckit
	(cd pyspeckit; git checkout teuben-gbt)
	@echo pip install -e pyspeckit

# the upstream
pyspeckit2:
	git clone https://github.com/pyspeckit/pyspeckit pyspeckit2

specviz:
	git clone https://github.com/spacetelescope/specviz

spectral-cube:
	git clone https://github.com/radio-astro-tools/spectral-cube

statcont:
	git clone https://github.com/radio-astro-tools/statcont

gbt-pipeline2:
	git clone https://github.com/GreenBankObservatory/gbt-pipeline gbt-pipeline2

# my development
gbt-pipeline:
	git clone https://github.com/teuben/gbt-pipeline
	(cd gbt-pipeline; git checkout python3)

gbtgridder:
	git clone https://github.com/GreenBankObservatory/gbtgridder

gbtpipe:
	git clone https://github.com/GBTSpectroscopy/gbtpipe

comb:
	git clone https://github.com/mpound/comb

gbtidl:
	wget https://sourceforge.net/projects/gbtidl/files/GBTIDL/2.10.1/gbtidl-2.10.1.tar.gz
	tar zxf gbtidl-2.10.1.tar.gz

asap:
	svn co http://svn.atnf.csiro.au/asap

asap-4.0.0:
	svn co http://svn.atnf.csiro.au/asap/tags/asap-4.0.0

lwa:
	svn co http://fornax.phys.unm.edu/lwa/subversion lwa


obit: 
	git clone  https://github.com/bill-cotton/Obit obit
