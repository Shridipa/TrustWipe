# keygen.py

from Crypto.PublicKey import RSA 

def generate_keys():
    # Generate a 2048-bit RSA key pair
    key = RSA.generate(2048)

    # Export private and public keys
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    # Save to .pem files 
    with open("private.pem", "wb") as priv_file:
        priv_file.write(private_key)

    with open("public.pem", "wb") as pub_file:
        pub_file.write(public_key)

    print("✅ RSA key pair generated and saved as 'private.pem' and 'public.pem'.")

# Run the function
if __name__ == "__main__":
    generate_keys()
 