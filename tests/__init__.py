from generators.AbstractGenerator import AbstractGenerator

from nistrng import SP800_22R1A_BATTERY
import os

BATTERY = SP800_22R1A_BATTERY
NUM_TESTS = 100

module_folder = os.path.abspath(__file__)[:-len(os.path.basename(__file__))]
results_folder = os.path.join(module_folder, "results")