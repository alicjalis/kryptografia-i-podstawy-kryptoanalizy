import hashlib
import secrets
from utils import get_p_256_params, EllipticCurve, modinv, generate_signature

p, a, b, G, n = get_p_256_params()
k = secrets.randbelow(n - 1) + 1
d = secrets.randbelow(n - 1) + 1
curve = EllipticCurve(p, a, b, G, n)

message1 = "first message"
r1, s1 = generate_signature(message1, d, curve, k)

message2 = "second message"
r2, s2 = generate_signature(message2, d, curve, k)

if r1 == r2:
    print("r1 and r2 are the same, potential nonce reuse vulnerability!")
else:
    print("r1 and r2 are different, no nonce reuse vulnerability.")
