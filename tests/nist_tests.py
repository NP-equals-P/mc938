from . import BATTERY

import nistrng

class NIST_tester:

    def __init__(self, generator):
        self.setup_pass_counts()

    def setup_pass_counts(self):
        self.pass_counts = {
            key: 0
            for key in BATTERY.keys()
        }
    
    def run_battery_tests(self, bits):
        outs = nistrng.run_all_battery(bits)
        results = [
            o[0] for o in outs
        ]
        battery_report = {
            test_name: {

            }
        }
