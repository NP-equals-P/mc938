from . import AbstractGenerator

from rule30 import random, Rule30Random
from numpy import array

class Rule30Generator(AbstractGenerator):

    def __init__(self):
        super().__init__()
        self.rng = Rule30Random()

    def generate_bytes(self, num_bytes):
        num = bin(self.rng.getrandbits(8*num_bytes))[2:]
        num = self.tab_byte_chain(num, num_bytes)
        num_arr = array([
            int(b) for b in num
        ])
        return num_arr
