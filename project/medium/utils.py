import hashlib
import secrets

p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff # duza liczba pierwsza uzywana do modulo
a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc # coeffs
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b # coeffs
G = (0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296, 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5) # starting point, generator cokolwiek to znaczy
n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551 # order
h = 0x1

def get_p_256_params():
    return p, a, b, G, n
def encrypt_message(message):
    sha_signature = \
        hashlib.sha256(message.encode()).hexdigest()
    return sha_signature

def modinv(a,p):
    # Extended Euclidean Algorithm
    return pow(a, -1, p)  #a**(-1) mod p


class EllipticCurve:
    def __init__(self, p, a, b, G, n):
        self.p = p
        self.a = a
        self.b = b
        self.G = G
        self.n = n

    def add(self, P, Q):
        if P == (None, None):
            return Q
        if Q == (None, None):
            return P

        x1, y1 = P
        x2, y2 = Q
        if x1 == x2 and y1 != y2:
            return (None, None)

        if P != Q:
            # λ = (y2 - y1) / (x2 - x1) mod p
            lam = ((y2 - y1) * modinv(x2 - x1, self.p)) % self.p
        else:
            # λ = (3x1² + a) / (2y1) mod p
            lam = ((3 * x1 * x1 + self.a) * modinv(2 * y1, self.p)) % self.p

        x3 = (lam * lam - x1 - x2) % self.p
        y3 = (lam * (x1 - x3) - y1) % self.p

        return(x3, y3)

    def multiply(self, k, P):
        result = (None, None)  # Punkt zerowy
        addend = P
        while k:
            if k & 1:
                result = self.add(result, addend)
            addend = self.add(addend, addend)
            k >>= 1
        return result


def generate_signature(message, private_key, curve, k=None):
    if k is None:
        k = secrets.randbelow(curve.n - 1) + 1

    z = int.from_bytes(hashlib.sha256(message.encode()).digest(), byteorder="big")

    # R = k * G
    R = curve.multiply(k, curve.G)
    r = R[0] % curve.n
    if r == 0:
        r = R[0] % curve.n

    # s = k⁻¹ (z + r * d) mod n
    s = (modinv(k, curve.n) * (z + r * private_key)) % curve.n
    if s == 0:
        s = (modinv(k, curve.n) * (z + r * private_key)) % curve.n

    return r, s

def verify_signature(message, r, s, public_key, curve):

    if r <= 0 or r >= curve.n or s <= 0 or s >= curve.n:
        return False

    z = int.from_bytes(hashlib.sha256(message.encode()).digest(), byteorder="big")
    w = modinv(s, curve.n)
    u1 = (z * w) % curve.n
    u2 = (r * w) % curve.n

    P = curve.add(curve.multiply(u1, curve.G), curve.multiply(u2, public_key))

    return P[0] % curve.n == r