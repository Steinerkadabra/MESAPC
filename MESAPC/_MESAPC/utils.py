import f90nml
import shutil
import os
import numpy as np
import subprocess as sp


class cd:
    """
    Directory changer. can change the directory using the 'with' keyword, and returns to the previous path
    after leaving intendation. Example:
    with cd("some/path/to/go"): # changing dir
        foo()
        ...
        bar()
    #back to old dir
    """
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def run_mesa(run_id):
    inlist = run_id.inlist
    output_dir = run_id.output_dir
    file = f90nml.read(inlist)
    shutil.copytree(run_id.work_dir, output_dir + run_id.dir)
    for key in run_id.controls_dict.keys():
        file["controls"][key]= run_id.controls_dict[key]
    for key in run_id.star_dict.keys():
        file["star_job"][key]= run_id.star_dict[key]
    file["controls"]["log_directory"] = "../LOGS/" + run_id.log_dir
    file.write(output_dir +  run_id.dir + "/inlist_project")
    os.mkdir(output_dir + "/LOGS/" + run_id.log_dir)
    f = open(output_dir + "/LOGS/" + run_id.log_dir + "/controls_dict.txt", "w")
    f.write(str(run_id.controls_dict))
    f.close()
    f = open(output_dir + "/LOGS/" + run_id.log_dir + "/star_dict.txt", "w")
    f.write(str(run_id.star_dict))
    f.close()
    with cd(output_dir + run_id.dir):
        sp.call("./clean", shell = True, stderr=sp.DEVNULL, stdout=sp.DEVNULL)
        sp.call("./mk", stderr=sp.DEVNULL, stdout=sp.DEVNULL)
        sp.call("./star", stderr=sp.DEVNULL, stdout=sp.DEVNULL)
    return


class run_identification():
    def __init__(self, dir, controls_dict, star_dict, log_dir, inlist, filebase_dir, output_dir, num_threads, work_dir):
        self.dir = dir
        self.controls_dict = controls_dict
        self.star_dict = star_dict
        self.log_dir = log_dir
        self.inlist = inlist
        self.filebase_dir = filebase_dir
        self.work_dir = work_dir
        self.output_dir = output_dir
        self.OMP_NUM_THREADS = num_threads

class run_info():
    def __init__(self, run_dict, run_number):
        self.run_dict = run_dict
        self.run_number = run_number

def read_values(string):
    if isinstance(string, list):
        return_list = []
        for input_element in range(len(string)):
            return_list.append(read_values(string[input_element]))
        return return_list
    input = string.split(",")
    if input[0] == "float":
        return [float(i) for i in input[1:]]
    elif input[0] == "int":
        return [int(i) for i in input[1:]]
    elif input[0] == "string":
        return input[1:]
    elif input[0] == "linspace":
        return np.linspace(float(input[1]), float(input[2]), int(input[3]))
    elif input[0] == "logspace":
        return 10**(np.linspace(np.log10(float(input[1])), np.log10(float(input[2])), int(input[3])))

def basics_default():
    b = {
        "num_threads": 2,
        "filebase" : os.environ["MESAPC_DIR"] + "/filebase/",
        "calculate_grid": True,
        "total_num_threads": 10,
        "inlist": "default",
        "work_dir": "default"
    }
    return b


def read_file(string):
    file = f90nml.read(string)
    b = basics_default()
    for key in file["basics"].keys():
        b[key] = file["basics"][key]
    grid = {}
    for key in file["grid"].keys():
        grid[key] = read_values(file["grid"][key])
    runs = []
    keys = list(file.keys())
    count = 1
    for r in range(len(keys)):
        if keys[r][0] == "r":
            run_dict = {}
            for key in file[keys[r]].keys():
                run_dict[key] = read_values(file[keys[r]][key])
            runs.append(run_info(run_dict, count))
            count +=1
    return b, grid, runs

