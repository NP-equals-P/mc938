from . import BATTERY, AbstractGenerator, results_folder
from .statistics import get_conf_interval, is_distr_uniform, is_in_conf_interval

import nistrng
import pickle as pck
import os
import numpy as np

class NIST_results:

    def __init__(
            self, 
            name, 
            results, 
            eligible,
            pass_eval,
            unif_eval,
            total_tests
    ):
        self.name = name
        self.passed = dict()
        self.eligible_count = dict()
        self.scores = dict()
        for test_name, res in results.items():
            self.passed[test_name] = res["passed"]
            self.eligible_count[test_name] = eligible[test_name]
            self.scores[test_name] = res["scores"]
        self.pass_eval = pass_eval
        self.unif_eval = unif_eval
        self.total_tests = total_tests
        
    def get_pass_count(self):
        return self.passed
    
    def get_scores(self):
        return self.scores
    
    def get_eligible_count(self):
        return self.eligible_count
    
    def get_pass_eval(self):
        return self.pass_eval
    
    def get_unif_eval(self):
        return self.unif_eval
    
    def get_name(self):
        return self.name
    
    def get_total_tests(self):
        return self.total_tests

class NIST_tester:

    def __init__(self):
        self.setup_pass_counts()

    def setup_pass_counts(self):
        self.pass_counts = {
            key: 0
            for key in BATTERY.keys()
        }

    def set_report(self):
        self.tests = BATTERY.keys()

        self.test_keys_by_val = dict()
        for name, test in BATTERY.items():
            self.test_keys_by_val[test.name] = name
        self.stat_results = {
            test_name: {
                'passed': 0,
                'scores': np.array([])
            }
            for test_name in self.tests
        }
    
    def run_battery_tests(self, bits):
        outs = nistrng.run_all_battery(bits, BATTERY)
        results = [
            o[0] if o is not None else o for o in outs
        ]
        return results

    def run_statistic_tests(
            self, 
            gen:AbstractGenerator, 
            num_times=100,
            num_bytes=128,
            write_mode = 'w'
    ):
        self.set_report()
        eligible_count = {
            test_name: 0
            for test_name in self.tests
        }
        test_names = list(self.tests)
        gen_name = type(gen).__name__

        keys_path = os.path.join(results_folder, f"{gen_name}_keys.csv")
        with open(keys_path, write_mode) as f:
            for _ in range(num_times):
                bits = gen.generate_bytes(num_bytes)
                f.write(f"{"".join(bits.astype(str))}\n")
                result = self.run_battery_tests(bits)
                for i in range(len(self.tests)):
                    res = result[i]
                    if res is not None:
                        test_name = self.test_keys_by_val[res.name]
                        eligible_count[test_name] += 1
                        self.stat_results[test_name]['passed'] += \
                            res.passed
                        self.stat_results[test_name]['scores'] = \
                            np.append(
                                self.stat_results[test_name]['scores'],
                                res.score
                            )
                    
        scores_path = os.path.join(results_folder, f"{gen_name}_scores.csv")
        with open(scores_path, write_mode) as f:
            for test_name in test_names:
                if eligible_count[test_name] > 0:
                    f.write(f"{test_name}")
                    for score in self.stat_results[test_name]['scores']:
                        f.write(f", {score}")
                    f.write("\n")
        
        test_passes = np.array([self.stat_results[t]['passed'] for t in test_names])
        el_count = np.array([eligible_count[t] for t in test_names])
        pass_eval_list = is_in_conf_interval(test_passes, el_count)
        pass_eval = {
            test_names[i]: pass_eval_list[i]
            for i in range(len(test_names))
        }
        unif_eval = {
            t: is_distr_uniform(self.stat_results[t]['scores'])
            for t in test_names
        }

        results = NIST_results(gen_name, self.stat_results, eligible_count, pass_eval, unif_eval, num_times)
        with open(os.path.join(results_folder, f"{results.get_name()}_stat_test.pck"), 'wb') as f:
            pck.dump(results, f)
        return results
        
