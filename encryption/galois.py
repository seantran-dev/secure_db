# Galois field operations that I do not yet truly understand

def x(byte):
    byte <<= 1
    if byte & 0x100:
        byte ^= 0x11B
    return byte & 0XFF

def multiply(multiplier, byte):
    x2 = x(byte)
    x4 = x(x2)
    x8 = x(x4)

    if multiplier == 1:
        return byte
    elif multiplier == 2:
        return x(byte)
    elif multiplier == 3:
        return x(byte) ^ byte
    elif multiplier == 9:
        return x8 ^ byte
    elif multiplier == 11:
        return x8 ^ x2 ^ byte
    elif multiplier == 13:
        return x8 ^ x4 ^ byte
    elif multiplier == 14:
        return x8 ^ x4 ^ x2
    else:
        raise ValueError("Unsupported multiplier")
    

