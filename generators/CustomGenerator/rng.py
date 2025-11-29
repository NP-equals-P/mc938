from . import AbstractGenerator
from .webscraping import pickNewsPage, getTextFromG1
from .byte_search import getByteChain

def g1RNG(numBytes : int):
    """
    * Fetches a random news article from 'https://g1.globo.com' and randomly selects a specified number of bytes from its text, applying random transformations on each byte, composing a single string of bytes
    * Parameters:
    * * numBytes - Size of the pseudo-random number to be generated, in bytes
    """
    url = pickNewsPage()
    text = getTextFromG1(url)
    byteChain = getByteChain(text, numBytes)
    return byteChain

class g1RandomNumberGenerator(AbstractGenerator):

    def __init__(self):
        super().__init__()

    def generate_bytes(self, num_bytes):
        url = pickNewsPage()
        text = getTextFromG1(url)
        byteChain = getByteChain(text, num_bytes)
        return self.convert_str_to_array(byteChain)
