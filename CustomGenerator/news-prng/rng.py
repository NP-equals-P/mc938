from .webscraping import pickNewsPage, getTextFromG1
from .byte_search import getByteChain

def g1RandomNumberGenerator(numBytes : int):
    """
    * Fetches a random news article from 'https://g1.globo.com' and randomly selects a specified number of bytes from its text, applying random transformations on each byte, composing a single string of bytes
    * Parameters:
    * * numBytes - Size of the pseudo-random number to be generated, in bytes
    """
    url = pickNewsPage()
    text = getTextFromG1(url)
    byteChain = getByteChain(text, numBytes)
    return byteChain
