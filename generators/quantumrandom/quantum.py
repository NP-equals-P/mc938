from . import min_byte, max_byte, max_working, AbstractGenerator

from quantumrandom import randint

class QuantumGenerator(AbstractGenerator):

    def __init__(self):
        super().__init__()

    def _generate_byte(self):
        byte = ""
        for _ in range(2):
            r_int = round(randint(min_byte, max_working))
            byte += bin(r_int)[2:]
        r_int = round(randint(min_byte, 3))
        byte += bin(r_int)[2:]
        return byte

    def generate_bytes(self, num_bytes):
        byte_chain = ""
        for i in range(num_bytes):
            byte_chain += self._generate_byte()
        return self.convert_str_to_array(byte_chain)