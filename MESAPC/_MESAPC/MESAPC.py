import os
import sys
import MESAPC._MESAPC.MESAPC_grid as MESAPC_grid
import MESAPC._MESAPC.utils as utils
import shutil


class MESAPC():
    def __init__(self,  output_dir = None, grid = None, inlist = "default",  runs = None, NUM_THREADS = os.environ["OMP_NUM_THREADS"] ):
        self.controls_list = None
        self.star_list = None
        if output_dir == None and grid == None:
            try:
                basics, grid, runs = utils.read_file("inlist_MESAPC")
            except FileNotFoundError:
                sys.exit("FATAL: No inlist_MESAPC in current directory. If you are wokring with the MESAPC class, you will have to at least give the output dir and grid dictionary.")
            try:
                self.output_dir = basics["output_dir"] + "/"
            except:
                sys.exit("FATAL: output dir not specified in_MESAPC.")
            self.calculate_grid = basics["calculate_grid"]
            self.NUM_THREADS = basics["num_threads"]
            self.TOTAL_NUM_THREADS=basics["total_num_threads"]
            self.runs = runs
            self.inlist = basics["inlist"]
            self.work_dir = basics["work_dir"]
            self.grid = grid
        else:
            self.output_dir = output_dir + "/"
            self.NUM_THREADS = NUM_THREADS
            self.grid = grid
            self.runs = []
            if runs != None:
                for r in range(len(runs)):
                    self.runs.append(utils.run_info(runs[r], r+1))
            self.inlist = inlist
        try:
            os.mkdir(self.output_dir)
        except FileExistsError:
            sys.exit(
                "FATAL: output dir already exist!")
        os.mkdir(self.output_dir + "/LOGS/")
        os.environ["OMP_NUM_THREADS"] = str(self.NUM_THREADS)
        self.grid = self.get_grid(self.grid)
        self.filebase_dir = os.environ["MESAPC_DIR"] + "/filebase/"
        if self.work_dir == "default":
            self.work_dir = os.environ["MESAPC_DIR"] + "/filebase/work"
        if self.inlist == "default":
            self.inlist = self.filebase_dir + "inlist_project"
        shutil.copy(self.inlist, self.output_dir + "LOGS/")
        if output_dir == None and grid == None:
            shutil.copy("inlist_MESAPC", self.output_dir + "LOGS/")
        if self.calculate_grid:
            self.grid.run_all()
        else:
            for r in self.runs:
                self.grid.run(r)

    def default_lists(self, type):
        defaults = open(os.environ["MESA_DIR"] + f"/star/defaults/{type}.defaults", 'r')
        Lines = defaults.readlines()
        pvals = []
        for line in Lines:
            line = line.strip()
            if len(line) == 0:
                continue
            if line[0] != "!":
                line=line.split("(")[0].lower()
                pvals.append(line.split(" ")[0].lower())
        return pvals

    def split_dict(self, grid, run={}, output="array"):
        if self.controls_list == None:
            self.controls_list = self.default_lists("controls")
            self.star_list = self.default_lists("star_job")
        c_dict = {}
        c_names = []
        c_vals = []
        s_dict = {}
        s_names = []
        s_vals = []
        if len(run.keys()) == 0:
            for key in grid.keys():
                if key in self.controls_list:
                    c_dict[key] = grid[key]
                    c_names.append(key)
                    c_vals.append(grid[key])
                elif key in self.star_list:
                    s_dict[key] = grid[key]
                    s_names.append(key)
                    s_vals.append(grid[key])
                else:
                    sys.exit(f"FATAL: {key} is no possible parameter for MESA!")
        if output == "array":
            return c_names, c_vals, s_names, s_vals
        elif output == "dict":
            return c_dict, s_dict

    def get_grid(self, grid):
        c_names, c_vals, s_names, s_vals = self.split_dict(grid)
        return MESAPC_grid.MESAPC_grid(self, c_names, c_vals, s_names, s_vals)
