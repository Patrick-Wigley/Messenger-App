import rsa
from KeyGen import (produce_private_key,
                     produce_public_key,
                       get_process_pub)


# Utilised by client

def encrypt(data, pub_key):
    encrypted_data = rsa.encrypt(data.encode(), pub_key)
    return encrypted_data

def decrypt(data, priv_key):
    decrypted_data = rsa.decrypt(data, priv_key)
    return decrypted_data

if __name__ == "__main__":
    # NOTE - Definitley not finished.

    # Generate keys
    #private = produce_private_key()
    #public = produce_public_key(private)

    public, private = rsa.newkeys(555)

    print(f"KEYS:\nPrivate Key = {private}\nPublic Key = {public}\n####")
    #### Would send the private key ONCE to client

    # Encrypt data
    data = "hello fart"

    enc_data = encrypt(data, public)
    print(f"Encrypted data = {enc_data}")

    dec_data = decrypt(enc_data, private)
    print(f"Data recv decrypted = {dec_data}")

