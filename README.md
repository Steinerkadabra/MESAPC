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
To run MESAPC activate your environment. Then just use 
```bash
python $MESAPC_DIR/run.py
``` 
Similar to [MESA](http://mesa.sourceforge.net/), the input needed is a FORTRAN namelist file. It looks for a file called inlist_MESAPC. The basic structure is the following:


```fortran
&basics
    output_dir = "wherever you want the output to be saved"
/

&grid
    initial_mass = "linspace,1,10,100"
/

``` 

The namelist basics defines the global parameters for the grid. At least you will have to specify the output directory. For a list of all options see section "basics defaults".

The namelist grid describes the paramaters on which to calculate the grid. The grid will be sampled over all inputs in the grid namelist. The given example is to calculate a grid of 100 stellar models with linearly spaced masses between 1 and 10 solar masses. Any `<star_job>` or `<controls>` input that is allowed for MESA calculations can be used here. You have different options to enter values. The input has to be a string in the following form (all values are separated by a comma ,):
* **type declaration**
     * for a list of strings write: string
     * for a list of int write: int
     * for a list of float write: float
     * for a linearly spaced list of float values use: linspace (numpy linspace is used to create the list)
* **input values**
     * for a list just type the values separated with a comma
     * for a linspace list type the elements of np.linspace(a, b, c) in the order a,b,c (again separated by a comma)
 
Examples can be found in filebase/example_inputs.

You can add any number of additional grid runs. These may be seen in the following way. The grid is equal to some standard model. If you then want to look at changes to the standard model you can add additional runs with i.e.

```fortran
&run1
    initial_zfrac = "int,4,5,6,7,8"
/

&run2
    mixing_length_alpha = "f,1,1.5,2"
/

``` 

The additional run will be sampled with the normal grid - but the run inputs for are added to the initial sampling. run1 will therefore result in the calculation of 100 models with linearly spaced masses in the range of 1 to 10 solar masses, each calculated for all initial_zfracs values 4 5 6 7 8. Consequently run2 will calculate all masses for different values of mixing length. 

# Output
MESAPC caluclates the grids as defined in inlist_MESAPC. During the evolution you will see a `<tqdm>` progress bar for each run. After the evolutionas have finished the `<output_dir>` will hold the following:
* **inlist_project**: The initial inlist project input file
* **LOGS**: a folder full of more folder. Each of the folders (called grid_1, grid_2, ...grid_N, run1_1 run1_2, ..., run1_M, run2_1, etc.) will hold the elements that would typically be hold by LOGS directory in a MESA folder. This means the history.data and profile.data files as specified in the inlist_project (Output might be changed for different runs by including this in the `<run>` namelists as lists with one entry). In addition, the folder will hold two textfiles showing what is different in this calculation in respect to the inlist_project file. One for the star_job namelist and one for the controls inlist.
* **multiple folders from the MESA evolutions**: For every MESA evolutionary run one folder has been created. COMING SOON: option to delete this folders.

# basic namelist
The `<bsic>` namelist has the follwing options:
* NUM_THREADS: Defines the number of threads used for a single MESA calculation (default 2)
* TOTAL_NUM_THREADS: Defines the total number of threads MESAPC can use. Together with NUM_THREADS, this defines how much calculation can be run in parallel. (default 10)
* calculate_grid: If True then calculate the grid. If false, only the runs will be calculated (default True)
* inlist: The default inlist is given in filebase/inlist_project. It creates a pre-main-sequence model and calculates the evolution until the ZAMS (central hydrogen below 0.68). To change the inlist, just give the full path to your inlist. 


