from generators.AbstractGenerator import AbstractGenerator
from generators.CustomGenerator.rng import g1RandomNumberGenerator
from generators.rule30_gen.rule30 import Rule30Generator
from generators.json_rpc.json_rpc_gen import JSONRPCGenerator

from nistrng import SP800_22R1A_BATTERY
import os

BATTERY = SP800_22R1A_BATTERY
NUM_TESTS = 100

module_folder = os.path.abspath(__file__)[:-len(os.path.basename(__file__))]
results_folder = os.path.join(module_folder, "results")

tested_generators = [
    g1RandomNumberGenerator(),
    Rule30Generator(),
    JSONRPCGenerator()
]