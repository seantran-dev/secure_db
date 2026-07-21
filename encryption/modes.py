# AES encryption modes (ECB, CBC, CTR)

from . import utils
from . import aes
import os

# [ECB]: electronic codebook (one block at a time, independently)
def encrypt_ECB(data, roundkey):
    
    plaintext = utils.pad(data)

    ciphertext = b""
    for i in range(0, len(plaintext), 16):
        block = plaintext[i:i+16]
        ciphertext += aes.encrypt(block, roundkey)
    return ciphertext

def decrypt_ECB(data, roundkey):
    if len(data) % 16 != 0:
        raise ValueError("Ciphertext length must be a multiple of 16 bytes.")
    
    plaintext = b""
    for i in range(0, len(data), 16):
        block = data[i:i+16]
        plaintext += aes.decrypt(block, roundkey)

    return utils.unpad(plaintext)

# [CBC]: cipher block chaining (adds IV and performs XOR of previous and current block)
def encrypt_CBC(data, roundkey, iv = None):
    if iv is None:
        iv = os.urandom(16)

    plaintext = utils.pad(data)
    ciphertext = b""
    previous = iv

    for i in range(0, len(plaintext), 16):
        block = plaintext[i:i+16]
        cipher = aes.encrypt(utils.xor(previous, block), roundkey)
        ciphertext += cipher
        previous = cipher

    return iv, ciphertext

def decrypt_CBC(data, roundkey, iv):
    if len(data) % 16 != 0:
            raise ValueError("Length of ciphertext must be a multiple of 16 bytes.")
    if iv is None:
        iv = data[:16]
        ciphertext = data[16:]
    else:
        if len(iv) % 16 != 0:
            raise ValueError("Length of ciphertext must be a multiple of 16 bytes.")
        else:
            ciphertext = data
    previous = iv
    plaintext = b""

    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i+16]
        decrypted = aes.decrypt(block, roundkey)
        plaintext += utils.xor(decrypted, previous)
        previous = block

    return utils.unpad(plaintext)

# [CTR]: uses nonce + counter to produce a different keystream for every block
def encrypt_CTR(data, roundkey, nonce = None):
    if nonce is None or len(nonce) != 12:
        nonce = os.urandom(12) 
    
    plaintext = data # padding not needed, xor applies to blocks shorter than 16-byte
    ciphertext = b""
    
    counter = 0
    for i in range (0, len(plaintext), 16):
        data_block = plaintext[i:i+16]
        counter_block = aes.encrypt(nonce + (counter).to_bytes(4, "big"), roundkey)
        ciphertext += utils.xor(counter_block, data_block)
        counter += 1

    return nonce, ciphertext

def decrypt_CTR(data, roundkey, nonce):
    if nonce is None: # No nonce specified requires it to be appended to front of data
        nonce = data[:12]
        ciphertext = data[12:]
    else:
        ciphertext = data
    plaintext = b""

    counter = 0
    for i in range(0, len(ciphertext), 16): # pretty much the exact same loop used in encryption
        data_block = ciphertext[i:i+16]
        counter_block = aes.encrypt(nonce + (counter).to_bytes(4, "big"), roundkey)
        plaintext += utils.xor(counter_block, data_block)
        counter += 1
    
    return plaintext