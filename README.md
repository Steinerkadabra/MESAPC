 ## MESAPC - Modules for Experiments in Astrophysics Python Controller
 
This is a library to calculate a grid (or multiple grids) of [MESA](http://mesa.sourceforge.net/) models in an easy way using a Python implementation. It is easy to use as standalone routine using a FORTRAN namelist input file as well as part of an extended code.

# Getting Started

[MESA](http://mesa.sourceforge.net/) is a one dimensional stellar evolution code widely used in stellar astrophysics (For more information please take a look at the intrument papers: [MESA I](https://ui.adsabs.harvard.edu/abs/2011ApJS..192....3P/abstract), [MESA II](https://ui.adsabs.harvard.edu/abs/2013ApJS..208....4P/abstract), [MESA III](https://ui.adsabs.harvard.edu/abs/2015ApJS..220...15P/abstract), [MESA IV](https://ui.adsabs.harvard.edu/abs/2018ApJS..234...34P/abstract) and [MESA V](https://ui.adsabs.harvard.edu/abs/2019ApJS..243...10P/abstract)). To run MESAPC you will need a working version of MESA. The installation of MESA and the corresponding MESA SDK is straightforward. A guide can be be found [here](http://mesa.sourceforge.net/prereqs.html). 

MESAPC makes use of of mulitple Python Library. To have this working properly, we strongly recommend working with a virtual environment. MESAPC has been developed in a Python 3.7 environment using the following packages:
* f90nml 1.1.2
* numpy 1.18.2
* os
* sys
* utils
* shutil
* itertools
* multiprocessing as mp
* utils
* tqdm 4.45.0

Older versions of these modules have not been tested. We don' know if they will work. 


If you have all the prerequisites installes, just clone the repository and set the environmet varibale MESA_DIR to the directory you are ready to go. If you cloned the repository in i.e. /home/user/Projects then set the environment variable using
export MESAPC_DIR=/home/user/Projects/MESAPC

# Usage
Similar to [MESA](http://mesa.sourceforge.net/), the input needed is a FORTRAN namelist file. The basic structure is the following:


```fortran
&basics
    output_dir = "wherever you want the output to be saved"
/

&grid
    initial_mass = "linspace,1,10,100"
/

``` 

The namelist basics defines the global parameters for the grid. At least you will have to specify the output directory. For a list of all options see section "basics defaults".

The namelist grid describes the paramaters on which to calculate the grid. The given example is to calculate a grid of stellar models 
