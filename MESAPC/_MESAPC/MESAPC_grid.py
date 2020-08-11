import itertools
import multiprocessing as mp
import MESAPC._MESAPC.utils as utils
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
            vals_new  = []
            indices = []
            current_index = 0
            for val in self.control_vals:
                if isinstance(val[0], list):
                    indices_list = ()
                    for val2 in val:
                        vals_new.append(val2)
                        indices_list += (current_index, )
                        current_index += 1
                    indices.append(indices_list)
                else:
                    vals_new.append(val)
                    current_index += 1
            c_names, c_vals, s_names, s_vals = self.parent.split_dict(run.run_dict)
            names = list(itertools.chain(self.control_names, self.star_names, c_names, s_names))
            vals = list(itertools.product(*vals_new, *self.star_vals, *c_vals, *s_vals))
            vals_new = []
            for tuple in vals:
                new_tuple = ()
                current_index =0
                current_array = []
                current_tuple = 0
                for element in tuple:
                    try:
                        if current_index in indices[current_tuple]:
                            current_array.append(element)
                            if len(current_array) == len(indices[current_tuple]):
                                new_tuple += (current_array,)
                                current_array = []
                                current_tuple +=1
                        else:
                            new_tuple += (element,)
                    except IndexError:
                        new_tuple += (element,)
                    current_index +=1
                vals_new.append(new_tuple)
            vals = vals_new
        else:
            vals_new  = []
            indices = []
            current_index = 0
            for val in self.control_vals:
                if isinstance(val[0], list):
                    indices_list = ()
                    for val2 in val:
                        vals_new.append(val2)
                        indices_list += (current_index, )
                        current_index += 1
                    indices.append(indices_list)
                else:
                    vals_new.append(val)
                    current_index += 1
            names = list(itertools.chain(self.control_names, self.star_names))
            # vals = list(itertools.product(*self.control_vals, *self.star_vals))
            vals = list(itertools.product(*vals_new, *self.star_vals))
            vals_new = []
            for tuple in vals:
                new_tuple = ()
                current_index =0
                current_array = []
                current_tuple = 0
                for element in tuple:
                    try:
                        if current_index in indices[current_tuple]:
                            current_array.append(element)
                            if len(current_array) == len(indices[current_tuple]):
                                new_tuple += (current_array,)
                                current_array = []
                                current_tuple +=1
                        else:
                            new_tuple += (element,)
                    except IndexError:
                        new_tuple += (element,)
                    current_index +=1
                vals_new.append(new_tuple)
            vals = vals_new
        for i in range(len(vals)):
            d = {}
            for j in range(len(names)):
                d[names[j]] = vals[i][j]
            c, s = self.parent.split_dict(d, output="dict")
            if  run != None:
                r_id = utils.run_identification(f"run{run.run_number}_{i + 1}", c, s, f"run{run.run_number}_{i + 1}",
                                                self.parent.inlist, self.parent.filebase_dir, self.parent.output_dir, self.parent.NUM_THREADS, self.parent.work_dir)
            else:
                r_id = utils.run_identification(f"grid_{i+1}", c, s, f"grid_{i+1}", self.parent.inlist,
                                                self.parent.filebase_dir, self.parent.output_dir, self.parent.NUM_THREADS, self.parent.work_dir)
            MESA_runs.append(r_id)

        num = int(self.parent.TOTAL_NUM_THREADS/self.parent.NUM_THREADS)
        pool = mp.Pool(processes=num)
        for _ in tqdm.tqdm(pool.imap_unordered(utils.run_mesa, MESA_runs), total=len(MESA_runs), smoothing=0):
            pass

    def run_all(self):
        self.run()
        for r in self.parent.runs:
            self.run(r)