import hashlib
import secrets

from utils import modinv, get_p_256_params, EllipticCurve, generate_signature

def batch_verify(signatures, messages, public_keys, curve):
    if not (len(signatures) == len(messages) == len(public_keys)):
        raise ValueError("Mismatch in number of signatures, messages, or public keys.")

    combined_left = (None, None)
    combined_right = (None, None)

    for (r, s), m, pk in zip(signatures, messages, public_keys):
        if r <= 0 or r >= curve.n or s <= 0 or s >= curve.n:
            return False

        z = int.from_bytes(hashlib.sha256(m.encode()).digest(), byteorder="big")
        w = modinv(s, curve.n)

        # u1 = z * w mod n, u2 = r * w mod n
        u1 = (z * w) % curve.n
        u2 = (r * w) % curve.n

        # Combine u1*G and u2*PK into one sum
        part1 = curve.multiply(u1, curve.G)
        part2 = curve.multiply(u2, pk)
        point = curve.add(part1, part2)

        if point == (None, None) or point[0] % curve.n != r:
            return False

    return True

p, a, b, G, n = get_p_256_params()
curve = EllipticCurve(p, a, b, G, n)

# Generate key pair
priv = secrets.randbelow(n - 1) + 1
pub = curve.multiply(priv, G)

# Sign multiple messages
messages = ["hello", "test", "batch"]
signatures = [generate_signature(m, priv, curve) for m in messages]
public_keys = [pub for _ in messages]

# Batch verify
print(batch_verify(signatures, messages, public_keys, curve))  # Should print True
