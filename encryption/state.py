# Functions relating to state conversion

# convert 16-byte hexadecimal plaintext into 4x4 matrix (state)

def hex_to_state(hex_string):
    state = [[0 for _ in range(4)] for _ in range(4)]

    for row in range(4):
        for col in range(4):
            byte_index = (row + 4 * col) * 2

            # index increments by 4 * 2 = 8 for each row
            state[row][col] = int(hex_string[byte_index:byte_index + 2], 16)

    return state

# convert state to hexadecimal
def state_to_hex(state):
    hex_bytes = []

    for row in range(4):
        for col in range(4):
            byte = state[col][row]
            hex_bytes.append(f"{byte:02X}")
    return "".join(hex_bytes)

def byte_to_state(data):
    state = [[0 for _ in range(4)] for _ in range(4)]

    for i in range(16):
            row = i % 4
            col = i // 4
            state[row][col] = data[i]

    return state

def state_to_bytes(state):
    data = bytearray()

    for col in range(4):
        for row in range(4):
            data.append(state[row][col])

    return bytes(data)

    
# print(hex_to_state(plaintext))
# print(state_to_hex(hex_to_state(plaintext)))