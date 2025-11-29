def getBinStr(n):
    """
    * Takes the standard python binary representation (n) of a number and returns a string with only its binary digits
    * Parameters:
    * * n (string) - The python binary representation of an integer
    """
    return bin(n)[2:]

def tabBinByte(bin):
    """
    * Tabs a binary number to the left to complete 8 digits
    * Parameters:
    * * bin (string) - Binary representation of an integer
    """
    if len(bin) < 8:
        return "0"*(8-len(bin)) + bin
    return bin

def getBinASCII(c):
    """
    * Gets the ASCII encoding of a char (c)
    """
    binStr = getBinStr(ord(c))
    return tabBinByte(binStr)

def reverseString(s):
    """
    * Returns given string reversed
    * Parameters:
    * * s (string)
    """
    idxMax = len(s) - 1
    revStr = ""
    for i in range(idxMax, -1, -1):
        revStr += s[i]
    return revStr

def invertBits(n):
    """
    * Changes every bit of given binary number
    * Parameters:
    * * n (string) - Representation of a binary number, with only its digits
    """
    operand2 = '1'*len(n)
    n_inverted = int(n, 2) ^ int(operand2, 2)
    return bin(n_inverted)[2:]

def swapBits(b, idx_1, idx_2):
    """
    * Swaps bits from a binary number between given positions
    * Parameters:
    * * b (str) - The binary number, without '0b'
    * * idx_1, idx_2 (int) - Positions to be swapped
    """
    idx_1, idx_2 = idx_1%len(b), idx_2%len(b)
    if idx_1 > idx_2:
        idx_1, idx_2 = idx_2, idx_1
    bit1, bit2 = b[idx_1], b[idx_2]
    if idx_1 != idx_2:
        return b[:idx_1] + bit2 + b[idx_1+1:idx_2] + bit1 + b[idx_2+1:]
    return b

def selectDigit(n, pos : int):
    """
    * Returns the digit of an integer at a specified position, as if it was a string
    * Parameters:
    * * n (int)
    * * pos (int) - Position of the digit.
    """
    n_str = str(n)
    digit = n_str[pos%len(n_str)]
    return int(digit)

def updateDigit(n, idx, idx_aux):
    """
    * Gets the digit of an integer 'n' at a specified position and the next position to be used
    * Parameters:
    * * n (int)
    * * idx (int) - Position of the digit
    * * idx_aux (int) - Position of an auxiliary digit to be used in the calculation of the next index
    * Returns:
    * * next_idx (int) - Index of the next iteration
    * * digit (int)  - Digit for the current iteration
    """
    digit = selectDigit(n, idx)
    aux = selectDigit(n, idx_aux)
    return (idx-digit)%len(str(n)) - aux + ((aux%2)==0), digit