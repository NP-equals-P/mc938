from . import AbstractGenerator

from rule30 import random, Rule30Random

class Rule30Generator(AbstractGenerator):

    def __init__(self):
        super().__init__()
        self.rng = Rule30Random()

    def generate_bytes(self, num_bytes):
        return self.rng.getrandbits(8*num_bytes)
