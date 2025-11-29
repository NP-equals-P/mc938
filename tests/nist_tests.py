from . import BATTERY, AbstractGenerator

import nistrng

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
            o[0] for o in outs
        ]
        return results

    def run_statistic_tests(
            self, 
            gen:AbstractGenerator, 
            num_times=100,
            num_bytes=128
    ):
        self.set_report()
        for _ in range(num_times):
            bits = gen.generate_bytes(num_bytes)
            result = self.run_battery_tests(bits)
            for test_name in self.tests:
                self.stat_results[test_name]['mean_score'] += \
                    result[test_name]['score']
                self.stat_results[test_name]['passed'] += \
                    result[test_name]['passed']
        for test_name in self.tests:
            self.stat_results[test_name]['mean_score'] /= num_times
        return self.stat_results
        
