# Main transformation operations for AES

from . import constants
from . import galois

plaintext = "00112233445566778899aabbccddeeff"

# Applys xor operation to state and round key; works for both encryption and decryption
def add_round_key(state, round_key):
    for row in range(4):
        for col in range(4):
            state[row][col] ^= round_key[col][row]

    return state

# ----------TRANSFORMS----------

# performs sub_bytes operation on state using sbox- returns state full of integers
def sub_bytes(state):
    for row in range(4):
        for col in range(4):
            state[row][col] = constants.SBOX[state[row][col]]
    return state

# performs left-circular shift operation on state rows
def shift_rows(state):
    state[0] = state[0][0:] + state[0][:0]
    state[1] = state[1][1:] + state[1][:1]
    state[2] = state[2][2:] + state[2][:2]
    state[3] = state[3][3:] + state[3][:3]
    return state


# performs mix_columns using galois field- don't really understand the operation but anyways...
def mix_columns(state):
    for col in range(4):
        col_0 = state[0][col]
        col_1 = state[1][col]
        col_2 = state[2][col]
        col_3 = state[3][col]

        state[0][col] = (
            galois.multiply(2, col_0) ^ 
            galois.multiply(3, col_1) ^ 
            col_2 ^ 
            col_3
        )
        state[1][col] = (
            col_0 ^ 
            galois.multiply(2, col_1) ^ 
            galois.multiply(3, col_2) ^ 
            col_3
        )
        state[2][col] = (
            col_0 ^ 
            col_1 ^ 
            galois.multiply(2, col_2) ^ 
            galois.multiply(3, col_3)
        )
        state[3][col] = (
            galois.multiply(3, col_0) ^ 
            col_1 ^ 
            col_2 ^ 
            galois.multiply(2, col_3)
        )
    return state

# ----------INVERSE TRANSFORMS----------

# same sub_bytes operation, only using inverse sbox
def inv_sub_bytes(state):
    for row in range(4):
        for col in range(4):
            state[row][col] = constants.INV_SBOX[state[row][col]]
    return state

# performs right-circular shift operation on state rows
def inv_shift_rows(state):
    state[0] = state[0][0:] + state[0][:0]
    state[1] = state[1][-1:] + state[1][:-1]
    state[2] = state[2][-2:] + state[2][:-2]
    state[3] = state[3][-3:] + state[3][:-3]
    return state

# uses inverse mixcolumns matrix (inverse x forward = identity)
def inv_mix_columns(state):
    for col in range(4):
        col_0 = state[0][col]
        col_1 = state[1][col]
        col_2 = state[2][col]
        col_3 = state[3][col]

        state[0][col] = (
            galois.multiply(14, col_0) ^
            galois.multiply(11, col_1) ^
            galois.multiply(13, col_2) ^
            galois.multiply(9,  col_3)
        )
        state[1][col] = (
            galois.multiply(9,  col_0) ^
            galois.multiply(14, col_1) ^
            galois.multiply(11, col_2) ^
            galois.multiply(13, col_3)
        )
        state[2][col] = (
            galois.multiply(13, col_0) ^
            galois.multiply(9,  col_1) ^
            galois.multiply(14, col_2) ^
            galois.multiply(11, col_3)
        )
        state[3][col] = (
            galois.multiply(11, col_0) ^
            galois.multiply(13, col_1) ^
            galois.multiply(9,  col_2) ^
            galois.multiply(14, col_3)
        )
    return state