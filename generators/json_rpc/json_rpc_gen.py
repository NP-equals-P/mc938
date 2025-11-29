from . import AbstractGenerator, API_KEY

from rdoclient import RandomOrgClient

class JSONRPCGenerator(AbstractGenerator):

    def __init__(self):
        self.gen = RandomOrgClient(API_KEY, blocking_timeout=2.0, http_timeout=10.0)

    def generate_bytes(self, num_bytes):
        nums = self.gen.generate_integers(num_bytes, 0, 255, base=2)
        bits = ''.join([str(n) for n in nums])
        return self.convert_str_to_array(bits)