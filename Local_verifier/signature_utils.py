from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def load_public_key(path: str):
    with open(path, "rb") as key_file:
        return serialization.load_pem_public_key(key_file.read())

def verify_signature(public_key, signature: bytes, message: bytes) -> bool:
    public_key.verify(
        signature,
        message,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return True