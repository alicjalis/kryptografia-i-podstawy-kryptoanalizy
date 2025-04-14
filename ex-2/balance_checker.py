class BalanceChecker:
    def __init__(self, boolean_functions):
        self.boolean_functions = boolean_functions

    def check(self):
        print("\n️balance check for  functions")
        for i, func in enumerate(self.boolean_functions):
            count_zeros = func.count(0)
            count_ones = func.count(1)
            balanced = count_zeros == count_ones

            print(f"Function {i + 1}: 0s = {count_zeros}, 1s = {count_ones} {'balanced' if balanced else 'not balanced'}")
