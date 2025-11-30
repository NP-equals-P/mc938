from . import BATTERY, AbstractGenerator

import nistrng

class NIST_results:

    def __init__(self, name, results, eligible):
        self.name = name
        self.passed = dict()
        self.mean_score = dict()
        self.eligible_count = dict()
        for test_name, res in results.items():
            self.passed[test_name] = res["passed"]
            self.mean_score[test_name] = res["mean_score"]
            self.eligible_count[test_name] = eligible[test_name]
        
    def get_pass_count(self):
        return self.passed
    
    def get_mean_score(self):
        return self.mean_score
    
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
                'mean_score': 0
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
            num_bytes=128
    ):
        self.set_report()
        eligible_count = {
            test_name: 0
            for test_name in self.tests
        }
        test_names = self.tests

        for _ in range(num_times):
            bits = gen.generate_bytes(num_bytes)
            result = self.run_battery_tests(bits)
            for i in range(len(self.tests)):
                res = result[i]
                if res is not None:
                    test_name = self.test_keys_by_val[res.name]
                    eligible_count[test_name] += 1
                    self.stat_results[test_name]['mean_score'] += \
                        res.score
                    self.stat_results[test_name]['passed'] += \
                        res.passed
                    
        for test in test_names:
            if eligible_count[test] > 0:
                self.stat_results[test]['mean_score'] /= \
                    eligible_count[test]
        return NIST_results(type(gen).__name__, self.stat_results, eligible_count)
        
