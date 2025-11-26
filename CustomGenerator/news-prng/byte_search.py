from . import processing as proc

from psutil import net_io_counters

def getChainFromTxt(text, idx=0, num=1):
    """
    * Searches for a specified number of consecutive bytes in a text, at a specified position
    * Parameters:
    * * text (string)
    * * idx (int) - Position from wich the chain of bytes will be extracted
    * * num (int) - Size of the chain of bytes to be extracted, in bytes
    """
    # FIXME - Tratamento de erros (índices não existentes)
    substring = text[idx:idx+num]
    return "".join([proc.getBinASCII(ch) for ch in substring])

def getByteChain(text : str, numBytes : int):
    """
    * Randomly extracts a specified number of bytes from the given text, randomly applying transformations on each byte.
    * Parameters:
    * * text - String from where the bytes will be extracted
    * * numBytes - Number of bytes to extract from the text
    * Returns:
    * * byteChain (str) - Chain of bytes randomly extracted from the text and transformed
    """
    remaining_bytes = numBytes
    byteChain = ""
    idx = 0
    max_idx = len(text) - 1
    while remaining_bytes > 0:
        net_read = net_io_counters()
        bytesOut, bytesIn = net_read.bytes_sent, net_read.bytes_recv
        idx += (-1)**(bytesOut%10) * (bytesIn%1000)
        idx = idx % max_idx # Ou len(text) ?
        curr_chain = getChainFromTxt(text, idx)
        # Último dígito
        if bytesOut%2 != 0:
            curr_chain = '1' + curr_chain[1:] # Troca o primeiro dígito por '1'
        # Penúltimo dígito
        if ((bytesOut%100)//10)%2 != 0:
            curr_chain = proc.reverseString(curr_chain) # Inverte a ordem dos bits
        # Antepenúltimo dígito
        if ((bytesOut%1000)//100)%2 != 0:
            curr_chain = proc.invertBits(curr_chain) # Troca a 'polaridade' de cada bit
        byteChain += proc.tabBinByte(curr_chain)
        remaining_bytes -= 1
    return byteChain