class SACChecker:
    def __init__(self, boolean_functions):
        self.boolean_functions = boolean_functions

    def compute_sac(self):
        print("\nStrict Avalanche Criterion (SAC) Check:")
        num_functions = len(self.boolean_functions)
        sac_results = [[0] * 8 for _ in range(num_functions)]

        # Przechodzimy przez każdą funkcję boolowską
        for f_index, func in enumerate(self.boolean_functions):
            for bit_pos in range(8):
                changes = 0
                for x in range(256):
                    flipped_x = x ^ (1 << bit_pos)
                    if func[x] != func[flipped_x]:
                        changes += 1

                sac_probability = changes / 256.0
                sac_results[f_index][bit_pos] = sac_probability

        for i, sac_values in enumerate(sac_results):
            formatted_probs = ", ".join(f"{p:.2f}" for p in sac_values)
            print(f"Function F{i + 1}: {formatted_probs}")

        # Średnie prawdopodobieństwo zmiany w całym bloku
        avg_sac = sum(sum(row) for row in sac_results) / (num_functions * 8)
        print(f"\nAverage SAC probability across all functions: {avg_sac:.4f}")

        return sac_results, avg_sac
