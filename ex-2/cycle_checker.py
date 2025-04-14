
class CycleChecker:
    def __init__(self, sbox):
        self.sbox = sbox

    def check_full_cycle(self):
        visited = set()
        current = 0

        for _ in range(len(self.sbox)):
            if current in visited:
                return False
            visited.add(current)
            current = self.sbox[current]


        return len(visited) == len(self.sbox) and current == 0

# zapisac dlugosc