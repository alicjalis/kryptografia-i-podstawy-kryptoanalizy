import hashlib

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec as crypto_ec
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
import secrets
import random
from utils import EllipticCurve, modinv, get_p_256_params

# Załaduj parametry krzywej P-256 z utils.py
p, a, b, G, n = get_p_256_params()
curve = EllipticCurve(p, a, b, G, n)


def hash_message(message: bytes) -> bytes:
    digest = hashes.Hash(hashes.SHA256())
    digest.update(message)
    return digest.finalize()


def convert_public_key_to_point(public_key):
    # Konwertuj klucz publiczny z cryptography na punkt (x, y)
    numbers = public_key.public_numbers()
    return (numbers.x, numbers.y)


def batch_verify(messages, signatures, public_keys):
    if not (len(messages) == len(signatures) == len(public_keys)):
        raise ValueError("messages, signatures, and public_keys must have same length")

    # Step 1: Basic signature checks
    for sig in signatures:
        try:
            r, s = decode_dss_signature(sig)
            if r <= 0 or r >= n or s <= 0 or s >= n:
                return False
        except:
            return False

    # Step 2: Compute random scalars
    random_scalars = [secrets.randbelow(n - 1) + 1 for _ in range(len(messages))]

    # Step 3: Compute intermediate values
    s_inv = []
    z_list = []
    pub_points = []
    r_list = []

    for msg, sig, pub_key in zip(messages, signatures, public_keys):
        r, s = decode_dss_signature(sig)
        z = int.from_bytes(hash_message(msg), byteorder="big") % n
        s_inv_val = modinv(s, n)
        s_inv.append(s_inv_val)
        z_list.append(z)
        r_list.append(r)

        # Convert public key to point
        pub_point = convert_public_key_to_point(pub_key)
        pub_points.append(pub_point)

    # Step 4: Compute aggregated values
    agg_R = (None, None)  # Point at infinity
    agg_r = 0

    for a_i, s_i, z_i, r_i, pub_point in zip(random_scalars, s_inv, z_list, r_list, pub_points):
        u1 = (z_i * s_i) % n
        u2 = (r_i * s_i) % n

        # Compute u1*G
        term1 = curve.multiply(u1, G)
        # Compute u2*P
        term2 = curve.multiply(u2, pub_point)
        # Compute u1*G + u2*P
        term = curve.add(term1, term2)
        # Compute a_i * (u1*G + u2*P)
        scaled_term = curve.multiply(a_i, term)

        # Aggregate points
        agg_R = curve.add(agg_R, scaled_term)
        # Aggregate r values
        agg_r = (agg_r + a_i * r_i) % n

    # Step 5: Final verification
    if agg_R == (None, None):
        return False

    return agg_R[0] % n == agg_r % n


# --- TESTING ---
if __name__ == "__main__":
    # Test 1: Verify single signature directly (sanity check)
    print("Sanity check - single signature verification")
    from utils import generate_signature, verify_signature

    # Generate key pair
    private_key = secrets.randbelow(n - 1) + 1
    public_key = curve.multiply(private_key, G)

    # Test message
    message = "Test message"
    z = int.from_bytes(hashlib.sha256(message.encode()).digest(), byteorder="big")

    # Generate signature
    r, s = generate_signature(message, private_key, curve)
    print(f"Single signature verification (should be True): {verify_signature(message, r, s, public_key, curve)}")

    # Test with wrong message
    print(f"Wrong message verification (should be False): {verify_signature('Wrong message', r, s, public_key, curve)}")

    # Test with wrong public key
    wrong_public_key = curve.multiply(private_key + 1, G)  # Different key
    print(f"Wrong key verification (should be False): {verify_signature(message, r, s, wrong_public_key, curve)}")
    print()

    # Test 2: All signatures are valid (using cryptography library)
    print("Test 2: All signatures valid")
    num_tests = 3
    private_keys = []
    public_keys = []
    messages = []
    signatures = []

    for i in range(num_tests):
        private_key = crypto_ec.generate_private_key(crypto_ec.SECP256R1())
        public_key = private_key.public_key()

        message = f"Hello world {i}".encode()

        signature = private_key.sign(message, crypto_ec.ECDSA(hashes.SHA256()))

        private_keys.append(private_key)
        public_keys.append(public_key)
        messages.append(message)
        signatures.append(signature)

    valid = batch_verify(messages, signatures, public_keys)
    print(f"Batch verification result (should be True): {valid}")
    print()

    # Test 3: One invalid signature
    print("Test 3: One invalid signature")
    messages = [f"Test message {i}".encode() for i in range(num_tests)]
    signatures = [priv.sign(msg, crypto_ec.ECDSA(hashes.SHA256())) for priv, msg in zip(private_keys, messages)]

    # Corrupt one signature
    corrupt_idx = random.randint(0, num_tests - 1)
    corrupted_sig = bytearray(signatures[corrupt_idx])
    corrupted_sig[10] ^= 0xFF
    signatures[corrupt_idx] = bytes(corrupted_sig)

    valid = batch_verify(messages, signatures, public_keys)
    print(f"Batch verification result (should be False): {valid}")
    print()

    # Test 4: Single signature verification (special case of batch)
    print("Test 4: Single signature verification")
    message = b"Single message test"
    signature = private_keys[0].sign(message, crypto_ec.ECDSA(hashes.SHA256()))

    valid = batch_verify([message], [signature], [public_keys[0]])
    print(f"Single signature verification result (should be True): {valid}")

    # Test with wrong public key
    valid = batch_verify([message], [signature], [public_keys[1]])
    print(f"Single signature with wrong key (should be False): {valid}")