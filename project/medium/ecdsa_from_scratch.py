import hashlib
import secrets
from utils import get_p_256_params, EllipticCurve, modinv, generate_signature, verify_signature


p, a, b, G, n = get_p_256_params()
curve = EllipticCurve(p, a, b, G, n)

private_key = secrets.randbelow(n - 1) + 1  # prywatny klucz
public_key = curve.multiply(private_key, G)

# creating the signature
message = "ecdsa testing"
r, s = generate_signature(message, private_key, curve)

# verifying the signature
is_valid = verify_signature(message, r, s, public_key, curve)
if is_valid:
    print("signature is valid")
else:
    print("signature is invalid")
