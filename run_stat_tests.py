import os
import pickle as pck

from generators.CustomGenerator.rng import g1RandomNumberGenerator
from generators.rule30_gen.rule30 import Rule30Generator
from generators.json_rpc.json_rpc_gen import JSONRPCGenerator

from tests import results_folder
from tests.visualization import TestVisualizer
from tests.nist_tests import NIST_tester

def get_nist_res(tester:NIST_tester, tested_generators, overwrite=False):
    nist_results = []
    for gen in tested_generators:
        name = type(gen).__name__
        path = os.path.join(results_folder, f"{name}_stat_test.pck")
        if not os.path.isfile(path) or overwrite:
            nist_results.append(tester.run_statistic_tests(gen))
        else:
            with open(path, 'rb') as f:
                nist_results.append(pck.load(f))
    return nist_results

def __main__():

    tested_generators = [
        g1RandomNumberGenerator(),
        Rule30Generator(),
        JSONRPCGenerator()
    ]

    tester = NIST_tester()
    nist_results = get_nist_res(tester, tested_generators)
    visualizer = TestVisualizer(nist_results)
    for test in ["passed", "scores", "eligibility"]:
        visualizer.show_compared_stats(test, True)

__main__()