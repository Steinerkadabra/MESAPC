import os
import numpy as np
import matplotlib.pyplot as plt
import ast
import MESAPC._MESAPC.utils as utils
import time


def load_dict(file):
    with open(file, 'r') as file:
        data = file.read().replace('\n', '')
    return ast.literal_eval(data)


class DataHandler():
    def __init__(self, inlist = "inlist_MESAPC"):
        basics, grid, runs = utils.read_file(inlist)
        self.basics = basics
        self.output_dir = basics["output_dir"]
        self.grid = None
        self.runs = []
        self.run_infos = runs
        self.num_runs = len(runs)
        self.load_data()

    def load_data(self):
        if self.basics["calculate_grid"]:
            self.grid = data_grid("grid", self.output_dir)
        for j in range(1, self.num_runs +1):
            self.runs.append(data_grid(f"run{j}", self.output_dir))

    def load_hists(self):
        if self.basics["calculate_grid"]:
            self.grid.load_hists()
        for run in self.runs:
            run.load_hists()

    def refresh_files(self):
        if self.basics["calculate_grid"]:
            self.grid.refresh_files()
        for run in self.runs:
            run.refresh_files()


class data_grid():
    def __init__(self, grid, output_dir):
        self.output_dir = output_dir
        self.grid_name = grid
        files = os.listdir(output_dir + '/LOGS')
        self.grid_files = [i for i in files if grid in i]
        self.grid_len = len(self.grid_files)
        self.data = []
        for i in range(1, self.grid_len + 1):
            self.data.append(evol_data(self.output_dir + '/LOGS/' + f"{grid}_{i}/"))

    def refresh_files(self):
        files = os.listdir(self.output_dir + '/LOGS')
        grid_files = [i for i in files if self.grid_name in i]
        for i in range(self.grid_len+ 1, len(grid_files) + 1):
            self.data.append(evol_data(self.output_dir + '/LOGS/' + f"{self.grid_name}_{i}/"))
        self.grid_files = grid_files
        self.grid_len = len(grid_files)
        return


    def load_hists(self):
        for evol in self.data:
            evol.load_hist()
        return

    def load_profiles(self):
        for evol in self.data:
            evol.load_profiles()
        return

    def plot_grid(self, ax, x, y, lw = 2, ls = '-', color = 'black', alpha = 1):
        for evol in self.data:
            if evol.hist_load_time != 0:
                ax.plot(evol.hist[x], evol.hist[y], lw = lw, ls =ls, color = color, alpha = alpha)
        return


class evol_data():
    def __init__(self, directory):
        self.controls =load_dict(directory + "controls_dict.txt")
        self.star_job =load_dict(directory + "star_dict.txt")
        self.dir = directory
        self.hist = None
        self.hist_keys = None
        self.hist_load_time = 0
        self.profiles = {}
        self.profile_keys = None

    def load_hist(self):
        try:
            savetime = os.path.getmtime(self.dir+ "history.data")
        except FileNotFoundError:
            return
        if savetime > self.hist_load_time:
            self.hist_load_time = savetime
            self.hist = np.genfromtxt(self.dir+ "history.data", skip_header =5, names = True)
            self.hist_keys = self.hist.dtype.names
        return

    def load_profiles(self):
        profiles = np.loadtxt(self.dir+ "profiles.index", skiprows= 1).T
        for profile_number in profiles[2]:
            self.load_profile(int(profile_number))
        return

    def load_profile(self, profile_number):
        self.profiles[f"profile{profile_number}"] =  np.genfromtxt(self.dir+ f"profile{profile_number}.data", skip_header =5, names = True)
        if self.profile_keys == None:
            self.profile_keys = self.profiles[f"profile{profile_number}"].dtype.names
        return

