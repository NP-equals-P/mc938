from numpy import array

class AbstractGenerator:

    def __init__(self):
        super().__init__()

    def generate_bytes(self, num_bytes):
        pass

    def convert_str_to_array(self, bit_string:str):
        bit_list = [int(bit) for bit in bit_string]
        return array(bit_list)