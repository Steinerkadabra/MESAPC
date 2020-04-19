import itertools
import multiprocessing as mp
import utils
import tqdm


class MESAPC_grid():
    def __init__(self, parent, c_names, c_vals, s_names, s_vals):
        self.parent = parent
        self.control_names = c_names
        self.control_vals = c_vals
        self.star_names = s_names
        self.star_vals = s_vals

    def run(self, run = None):
        MESA_runs = []
        if run != None:
            c_names, c_vals, s_names, s_vals = self.parent.split_dict(run.run_dict)
            names = list(itertools.chain(self.control_names, self.star_names, c_names, s_names))
            vals = list(itertools.product(*self.control_vals, *self.star_vals, *c_vals, *s_vals))
        else:
            names = list(itertools.chain(self.control_names, self.star_names))
            vals = list(itertools.product(*self.control_vals, *self.star_vals))
        for i in range(len(vals)):
            d = {}
            for j in range(len(names)):
                d[names[j]] = vals[i][j]
            c, s = self.parent.split_dict(d, output="dict")
            if  run != None:
                r_id = utils.run_identification(f"run{run.run_number}_{i + 1}", c, s, f"run{run.run_number}_{i + 1}",
                                                self.parent.inlist, self.parent.filebase_dir, self.parent.output_dir, self.parent.NUM_THREADS)
            else:
                r_id = utils.run_identification(f"grid_{i+1}", c, s, f"grid_{i+1}", self.parent.inlist,
                                                self.parent.filebase_dir, self.parent.output_dir, self.parent.NUM_THREADS)
            MESA_runs.append(r_id)

        num = int(self.parent.TOTAL_NUM_THREADS/self.parent.NUM_THREADS)
        pool = mp.Pool(processes=num)
        for _ in tqdm.tqdm(pool.imap_unordered(utils.run_mesa, MESA_runs), total=len(MESA_runs)):
            pass

    def run_all(self):
        self.run()
        for r in self.parent.runs:
            self.run(r)