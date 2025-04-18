from cryptography.hazmat.primitives import hashes

from cryptography.hazmat.primitives.asymmetric import ec

private_key = ec.generate_private_key(

    ec.SECP384R1()

)

data = b"this is some data I'd like to sign"
tampered_data = b"this is tampered data"

signature = private_key.sign(

    data,

    ec.ECDSA(hashes.SHA256())

)

public_key = private_key.public_key()

print("Test for data variable:")
try:
    public_key.verify(signature, data, ec.ECDSA(hashes.SHA256()))
    print("Signature is valid")
except:
    print("Signature is not valid")

print("Test fot tampered data:")
try:
    public_key.verify(signature, tampered_data, ec.ECDSA(hashes.SHA256()))
    print("Signature is valid")
except:
    print("Signature is not valid")


