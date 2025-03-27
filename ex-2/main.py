from balance_checker import BalanceChecker
from sbox_utils import load_sbox, print_sbox, extract_boolean_functions, print_boolean_functions

def main():
    # File path
    sbox_file = "sbox_08x08_20130110_011319_02.SBX"

    # Load S-box
    sbox = load_sbox(sbox_file)

    # Print S-box
    print_sbox(sbox)

    # Extract Boolean functions
    boolean_functions = extract_boolean_functions(sbox)

    # Print Boolean functions
    print_boolean_functions(boolean_functions)

    # Verify size (should be 256 values per function)
    assert all(len(f) == 256 for f in boolean_functions), "Error: Functions must have 256 values!"

    # Check balance using BalanceChecker
    balance_checker = BalanceChecker(boolean_functions)
    balance_checker.check()

if __name__ == "__main__":
    main()
