# packages
import numpy as np

# program imports
from . import state as st
from . import constants as const
from . import transforms as trans
from . import key_schedule as ks

# plaintext -> bytes -> state -> AES operation -> bytes --> ciphertext
def encrypt(plaintext, round_key):
    round_key = round_key.hex().upper()
    key_size = len(round_key * 4)
    if key_size == 128:
        Nr = 10
    elif key_size == 192:
        Nr = 12
    elif key_size == 256:
        Nr = 14
    else:
        raise ValueError("Invalid key size")

    
    #print("[AES-", end = "")
    #print(key_size, end = "]\n")


    state = st.byte_to_state(plaintext)

    round_keys = ks.generate_ks(round_key, key_size)

    # initial round
    state = trans.add_round_key(state, round_keys[0])

    # iterative rounds
    for i in range(1, Nr):
        state =  trans.sub_bytes(state)
        state = trans.shift_rows(state)
        state = trans.mix_columns(state)
        state = trans.add_round_key(state, round_keys[i])

    # final round
    state = trans.sub_bytes(state)
    state = trans.shift_rows(state)
    state = trans.add_round_key(state, round_keys[Nr])

    return st.state_to_bytes(state)

# ciphertext -> bytes -> state -> AES decrypt -> bytes --> plaintext
def decrypt(ciphertext, round_key):
    round_key = round_key.hex().upper()
    key_size = len(round_key * 4)
    if key_size == 128:
        Nr = 10
    elif key_size == 192:
        Nr = 12
    elif key_size == 256:
        Nr = 14
    else:
        raise ValueError("Invalid key size")
    
    state = st.byte_to_state(ciphertext)

    round_keys = ks.generate_ks(round_key, key_size)

    # initial round
    state = trans.add_round_key(state, round_keys[-1])

    # iterative rounds
    for i in range(Nr - 1, 0, -1):
        state = trans.inv_shift_rows(state)
        state = trans.inv_sub_bytes(state)
        state = trans.add_round_key(state, round_keys[i])
        state = trans.inv_mix_columns(state)
    # final round
    state = trans.inv_shift_rows(state)
    state = trans.inv_sub_bytes(state)
    state = trans.add_round_key(state, round_keys[0])
    
    return st.state_to_bytes(state)
        
        