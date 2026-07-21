# Key schedule creation
# Word: 4 bytes

from . import constants


# convert 16-byte hexadecimal roundkey into 4 words
def hex_to_words(roundkey, Nk):  
    words = [[0 for _ in range(4)] for _ in range(Nk)]

    for row in range(4):
        for col in range(Nk):
            byte_index = (row + 4 * col) * 2

            # index increments by 4 * 2 = 8 for each row
            words[col][row] = int(roundkey[byte_index:byte_index + 2], 16)
    return words 


# rotate word operation (left circular shift)
def rot_word(word):
    return word[1:] + word[:1]

# apply sbox to word
def sub_word(word):
    new_word = []
    for byte in word:
        new_word.append(constants.SBOX[byte])

    return new_word

# xor operation for two wrods
def xor_words(w1, w2):
    new_word = []

    for i in range(4):
        new_word.append(w1[i] ^ w2[i])

    return new_word


# Calculate the next round key
def generate_ks(round_key, key_size):

    if key_size == 128:
        Nk = 4
        Nr = 10
    elif key_size == 192:
        Nk = 6
        Nr = 12
    elif key_size == 256:
        Nk = 8
        Nr = 14
    else:
        raise ValueError("Invalid key size")

    words = hex_to_words(round_key, Nk)
    total_words = 4 * (Nr + 1)

    for i in range(Nk, total_words):

        temp = words[i - 1].copy()
        if i % Nk == 0:
            temp = rot_word(temp)
            temp = sub_word(temp)
            temp[0] ^= constants.RCON[i // Nk]

        elif Nk == 8 and i % Nk == 4:
            temp = sub_word(temp)

        new_word = xor_words(words[i - Nk], temp)
        words.append(new_word)

    round_keys = []

    for i in range(0, len(words), 4):
        round_keys.append(words[i:i+4])

    return round_keys

