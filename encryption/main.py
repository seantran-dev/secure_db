from . import state as st
from . import constants as const
from . import transforms as trans
from . import key_schedule as ks
from . import aes
from . import modes
from . import utils

import base64

# Input plaintext and roundkey
plaintext_hex = "48656c6c6f20576f726c642121212121" 
roundkey_hex =  "000102030405060708090A0B0C0D0E0F" # 101112131415161718191A1B1C1D1E1F
# Hello World!!!!!

plaintext =    b'\x48\x65\x6c\x6c\x6f\x20\x57\x6f\x72\x6c\x64\x21\x21\x21\x21\x21' # Hello World!!!!!
plaintext_16 = b'\x48\x65\x6c\x6c\x6f\x20\x57\x6f\x72\x6c\x64\x21\x21\x21\x21\x21' # Hello World!!!!!
roundkey = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'


def default():
    # testing with default cases
    print("[Text & Key | Input]")
    print("   Encryption Key:  ", end = " ")
    print(roundkey.hex().upper())
    print("   Plaintext:    ", end = "--> ")
    print(plaintext.hex().upper(), end =" <--")
    print("\n")

    # Default: performs operation on only one block (for simplicity, only use for 16-byte plaintext)
    print("[Single Block | Default]") 
    ciphertext = aes.encrypt(plaintext_16, roundkey)
    print("   Encryption:       ", end = "")
    print(ciphertext.hex().upper())

    decrypted_plaintext = aes.decrypt(ciphertext, roundkey)
    print("   Decryption:   ", end = "--> ")
    print(decrypted_plaintext.hex().upper(), end =" <--")
    print("\n")

# Custom: performs operations using modes
def custom():
    # -------- Electronic Codebook (ECB) --------
    print("[Electronic Codebook | ECB]")
    print("   Encryption:      ", end = " ")
    ciphertext = modes.encrypt_ECB(plaintext, roundkey).hex().upper()
    print(ciphertext)
    print("   Decryption:   ", end = "--> ")
    print(modes.decrypt_ECB(bytes.fromhex(ciphertext), roundkey).hex().upper(), end = " <--")
    print("\n")

    # -------- Cipher Block Chaining (CBC) --------
    print("[Cipher Block Chaining | CBC]")
    print("   Encryption:      ", end = " ") 
    iv_cbc = None # preset must be 16 bytes 
    encrypted_cbc = modes.encrypt_CBC(plaintext, roundkey, iv_cbc) # stores tuple of iv and ciphertext
    iv_cbc = encrypted_cbc[0]
    ciphertext_cbc = encrypted_cbc[1]
    print((ciphertext_cbc).hex().upper())

    print("           IV:      ", end = " ")
    print(iv_cbc.hex().upper())

    print("   Decryption:   ", end = "--> ")
    print(modes.decrypt_CBC(ciphertext_cbc, roundkey, iv_cbc).hex().upper(), end = " <--")
    print("\n")

    # -------- Counter Mode (CTR) --------
    print("[Counter Mode | CTR]")
    print("   Encryption:      ", end = " ") 
    nonce_ctr = None # preset must be 12 bytes
    encrypted_ctr = modes.encrypt_CTR(plaintext, roundkey, nonce_ctr)
    nonce_ctr = encrypted_ctr[0]
    ciphertext_ctr = encrypted_ctr[1]
    print((ciphertext_ctr).hex().upper())
    print("        Nonce:      ", end = " ")
    print(nonce_ctr.hex().upper())
    print("   Decryption:   ", end = "--> ")
    print(modes.decrypt_CTR(ciphertext_ctr, roundkey, nonce_ctr).hex().upper(), end =" <--")
    print("\n")


if __name__ ==  "__main__":
    default()
    custom()

