import itertools

class NonlinearityChecker:
    def __init__(self, boolean_functions):
        self.boolean_functions = boolean_functions
        self.affine_functions = self.generate_affine_functions()

    def generate_affine_functions(self):
        affine_functions = []
        # generuje wszystkie kombinacje - 256 możliwości
        for coeffs in itertools.product([0, 1], repeat=8):
            for c in [0, 1]:  # Stała c może być 0 lub 1
                affine_function = []
                for x in range(256):
                    x_bits = [(x >> i) & 1 for i in range(8)]
                    affine_value = sum(a * b for a, b in zip(coeffs, x_bits)) % 2
                    affine_function.append(affine_value ^ c)  # odwracanie funkcji
                affine_functions.append(affine_function)
        return affine_functions

    def hamming_distance(self, f, g):
        return sum(fi != gi for fi, gi in zip(f, g))

    def compute_nonlinearity(self):
        nonlinearity_values = []
        for i, f in enumerate(self.boolean_functions):
            min_hamming_dist = min(self.hamming_distance(f, a) for a in self.affine_functions)
            nonlinearity = min_hamming_dist
            nonlinearity_values.append(nonlinearity)
            print(f"Nonlinearity of F{i+1}: {nonlinearity}")
        return nonlinearity_values
