from . import BATTERY, AbstractGenerator, results_folder

import nistrng
import pickle as pck
import os
import numpy as np

class NIST_results:

    def __init__(self, name, results, eligible):
        self.name = name
        self.passed = dict()
        self.mean_score = dict()
        self.eligible_count = dict()
        self.scores = dict()
        for test_name, res in results.items():
            self.passed[test_name] = res["passed"]
            self.eligible_count[test_name] = eligible[test_name]
            self.scores[test_name] = res["scores"]
        
    def get_pass_count(self):
        return self.passed
    
    def get_scores(self):
        return self.scores
    
    def get_eligible_count(self):
        return self.eligible_count
    
    def get_name(self):
        return self.name

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
        test_names = self.tests
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
        
        results = NIST_results(gen_name, self.stat_results, eligible_count)
        with open(os.path.join(results_folder, f"{results.get_name()}_stat_test.pck"), 'wb') as f:
            pck.dump(results, f)
        return results
        
