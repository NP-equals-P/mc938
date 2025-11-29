from . import min_byte, max_byte, AbstractGenerator

from quantumrandom import randint

class QuantumGenerator(AbstractGenerator):

    def __init__(self):
        super().__init__()

    def generate_bytes(self, num_bytes):
        byte_chain = ""
        for i in range(num_bytes):
            new_byte = randint(
                min=min_byte,
                max=max_byte
            )
            byte_chain += bin(new_byte)[2:]
        return self.convert_str_to_array(byte_chain)