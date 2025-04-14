# macierz xorów - najpierw xor inputów do sboxa a potem
# xor tych samych outputów i pierwszy jest kolumna
# a drugi wierszem, i tam gdzie wyjdzie miejsce tam dodajesz 1

from sbox_utils import load_sbox, print_sbox, extract_boolean_functions, print_boolean_functions
import numpy as np

class XORProfileChecker:
    def __init__(self, sbox):
        self.sbox = sbox
        self.size = len(sbox)
        self.xor_profile = np.zeros((self.size, self.size), dtype=int)

    def compute_xor_profile(self):
        for i in range(self.size):
            for j in range(self.size):
                xor_input = i ^ j
                xor_output = self.sbox[i] ^ self.sbox[j]
                self.xor_profile[xor_input, xor_output] += 1
        # print("XOR profile: \n")
        # for row in self.xor_profile:
        #     print(" ".join(map(str,row)))


    def save_to_file(self, filename='xor_profile.txt'):
        with open(filename,"w") as f:
            for row in self.xor_profile:
                f.write(" ".join(map(str, row)) + "\n")


    def get_max_value(self):
        temp = np.copy(self.xor_profile)
        temp[0,0] = -1
        max_value = np.max(temp)
        return max_value



