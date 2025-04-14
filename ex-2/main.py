from balance_checker import BalanceChecker
from nonlinearity_checker import NonlinearityChecker
from sac_checker import SACChecker  # Importujemy SACChecker
from sbox_utils import load_sbox, print_sbox, extract_boolean_functions, print_boolean_functions
from xorprofile_checker import XORProfileChecker
from cycle_checker import CycleChecker
def main():
    sbox_file = "sbox_08x08_20130110_011319_02.SBX"

    sbox = load_sbox(sbox_file)
    #print_sbox(sbox)

    boolean_functions = extract_boolean_functions(sbox)
    #print_boolean_functions(boolean_functions)

    assert all(len(f) == 256 for f in boolean_functions), "Error: Functions must have 256 values!"

    balance_checker = BalanceChecker(boolean_functions)
    balance_checker.check()

    nonlinearity_checker = NonlinearityChecker(boolean_functions)
    nonlinearity_checker.compute_nonlinearity()

    sac_checker = SACChecker(boolean_functions)
    sac_checker.compute_sac()

    xor_checker = XORProfileChecker(sbox)
    xor_checker.compute_xor_profile()
    xor_checker.save_to_file("xor_profile.txt")

    max_value = xor_checker.get_max_value()
    print(f"XOR profile: {max_value}")

    cycle_checker = CycleChecker(sbox)
    is_full_cycle = cycle_checker.check_full_cycle()
    print(f"Full cycle check: {'PASSED' if is_full_cycle else 'FAILED'}")


if __name__ == "__main__":
    main()
