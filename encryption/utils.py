import os

# pads plaintext to achieve 16-byte blocks
def pad(data):
    padding = 16 - (len(data) % 16)
    return data + bytes([padding]) * padding

# unpads plaintext by removing initial padding
def unpad(data):
    padding_length = data[-1]

    # check if padding length is within valid range of 1 to 16 bytes
    # plaintext always pads additional bytes, never none, including 16 bytes exact
    if padding_length < 1 or padding_length > 16:
        raise ValueError("Invalid padding")
    
    # check if padding matches the specified length
    # ex. padding_length = 3, padding must be \x03\x03\x03, otherwise invalid
    if data[-padding_length:] != bytes([padding_length]) * padding_length:
         raise ValueError("Invalid padding")      
                             
    return data[:-padding_length]

def xor(block1, block2):
    return bytes(a ^ b for a, b in zip(block1, block2))