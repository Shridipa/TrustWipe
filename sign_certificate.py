# sign_certificate.py

import json
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA 
from Crypto.Hash import SHA256

# Load certificate 
with open("certificates/e842a1e7-f2ce-4640-8287-13f336dd4166.json", "r") as f:
    cert_data = f.read()
# Hash the certificate
hash_obj = SHA256.new(cert_data.encode()) 

# Load private key and sign 
private_key = RSA.import_key(open("private.pem").read())
signature = pkcs1_15.new(private_key).sign(hash_obj)

# Embed signature
cert_dict = json.loads(cert_data)
cert_dict["digital_signature"] = signature.hex()
 
# Save signed certificate 
with open("certificates/e842a1e7-f2ce-4640-8287-13f336dd4166.json", "w") as f:
    json.dump(cert_dict, f, indent=4)

print("✅ Certificate signed and saved.") 
 