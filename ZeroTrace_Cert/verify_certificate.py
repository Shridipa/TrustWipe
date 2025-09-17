import json
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256

with open("certificates/e842a1e7-f2ce-4640-8287-13f336dd4166.json", "r") as f:
    cert_dict = json.load(f)

signature = bytes.fromhex(cert_dict["digital_signature"])
cert_dict["digital_signature"] = None  # Remove before hashing
cert_data = json.dumps(cert_dict, indent=4)
hash_obj = SHA256.new(cert_data.encode())

public_key = RSA.import_key(open("public.pem").read())

try:
    pkcs1_15.new(public_key).verify(hash_obj, signature)
    print("✅ Signature is valid. Certificate is authentic.")
except (ValueError, TypeError):
    print("❌ Signature is invalid. Certificate may be tampered.")
