import numpy as np
from scipy.stats import chisquare

sac_matrix = np.loadtxt("matrix_des.txt")

# chi squared na jednowymiarowych danych
sac_values = sac_matrix.flatten()

bins = [0, 523857, 524158, 524417, 524718, 1048576]
observed_counts, _ = np.histogram(sac_values, bins=bins)

expected_counts = [820, 819, 818, 819, 820]

chi_stat, p_value = chisquare(observed_counts, expected_counts)

print(f"chi-Square statistic: {chi_stat:.4f}")
print(f"p-value: {p_value:.6f}")

if p_value < 0.01:
    print("p < 0.01")
else:
    print("p >= 0.01")
