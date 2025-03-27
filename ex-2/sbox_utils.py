def load_sbox(filename):
    with open(filename, "rb") as f:
        data = list(f.read())
    sbox = data[::2]  # step of 2 to skip zero bytes
    return sbox

def print_sbox(sbox):
    print("\n S-box (16×16 format):")
    for i in range(16):
        row = sbox[i * 16: (i + 1) * 16]
        print(" ".join(f"{x:02X}" for x in row))  # hex format to visualize it to myself

def extract_boolean_functions(sbox):
    boolean_functions = [[] for _ in range(8)]  # 8 lists for 8 functions

    print("\nExtracting Boolean Functions (Bitwise Representation):")
    for index, value in enumerate(sbox):
        binary_value = format(value, '08b')  # Convert to 8-bit binary string
        print(f"Input {index:3d} → Output {value:3d} ({binary_value})")  # Show bitwise mapping
        for i in range(8):
            boolean_functions[i].append(int(binary_value[i]))  # Extract each bit

    return boolean_functions

def print_boolean_functions(boolean_functions):
    print("\nFirst 16 values of each Boolean function:")
    for i, func in enumerate(boolean_functions):
        print(f"F{i + 1}: " + "".join(map(str, func[:16])) + "...")  # Print first 16 bits
