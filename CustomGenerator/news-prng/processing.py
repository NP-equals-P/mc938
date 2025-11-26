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