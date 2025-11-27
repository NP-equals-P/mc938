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
    i_1, i_2, i_3 = -1, -2, -4
    while remaining_bytes > 0:
        net_read = net_io_counters()
        bytesOut, bytesIn = net_read.bytes_sent, net_read.bytes_recv
        # Embaralha os dígitos de bytesOut
        for i in [i_1, i_2, i_3]:
            bytesOut = proc.swapBits(str(bytesOut), i, -i)
        bytesOut = int(bytesOut)
        # Atualiza os dígitos sorteados e os índices dos próximos dígitos
        i_1, d_1 = proc.updateDigit(bytesOut, i_1, i_3-i_2)
        i_2, d_2 = proc.updateDigit(bytesOut, i_2, i_1-i_3)
        i_3, d_3 = proc.updateDigit(bytesOut, i_3, i_2-i_1)
        # Atualiza o 'cursor' do byte a ser obtido da string ('text')
        idx += (-1)**(d_1) * (bytesIn%1000)
        idx = idx % max_idx # Ou len(text) ?
        curr_chain = getChainFromTxt(text, idx) # Obtém o byte a partir de 'text'
        # Último dígito
        if d_1%2 != 0:
            curr_chain = '1' + curr_chain[1:] # Troca o primeiro dígito por '1'
        # Penúltimo dígito
        if d_2%2 != 0:
            curr_chain = proc.reverseString(curr_chain) # Inverte a ordem dos bits
        # Antepenúltimo dígito
        if d_3%2 != 0:
            curr_chain = proc.invertBits(curr_chain) # Troca a 'polaridade' de cada bit
        curr_chain = proc.tabBinByte(curr_chain)
        # Troca aleatória de bits
        curr_chain = proc.swapBits(curr_chain, d_1, d_2)
        byteChain += curr_chain
        remaining_bytes -= 1
    return byteChain
        