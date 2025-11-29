from numpy import array

class AbstractGenerator:

    def __init__(self):
        super().__init__()

    def generate_bytes(self, num_bytes):
        pass

    def convert_str_to_array(self, bit_string:str):
        bit_list = [int(bit) for bit in bit_string]
        return array(bit_list)
    
    def tab_byte_chain(self, byte_chain:str, num_bytes=1):
        total_bits = 8*num_bytes
        if len(byte_chain) < total_bits:
            return '0'*(total_bits-len(byte_chain)) + byte_chain
        return byte_chain