import rsa
import rsa.key
from Shared.Encryption.KeyGen import (produce_private_key,
                     produce_public_key,
                       get_process_pub)


# Utilised by client

def encrypt(data, pub_key):
    encrypted_data = rsa.encrypt(data.encode("utf-8"), pub_key)
    return encrypted_data

def decrypt(data, priv_key) -> bytes: 
    decrypted_data = rsa.decrypt(data, priv_key)
    return decrypted_data

def get_pub_priv_key():
    return rsa.newkeys(2048)

def convert_to_key_from_pkcs(pub_pkcs, priv_pkcs):
    pub = rsa.key.PublicKey.load_pkcs1(pub_pkcs, format="DER")
    priv = rsa.key.PrivateKey.load_pkcs1(priv_pkcs, format="DER")
    return pub, priv


if __name__ == "__main__":
    # NOTE - Definitley not finished.

    # Generate keys
    #private = produce_private_key()
    #public = produce_public_key(private)

    public, private = get_pub_priv_key()

    print(f"KEYS:\nPrivate Key = {private}\nPublic Key = {public}\n####")
    #### Would send the private key ONCE to client

    # Encrypt data
    data = "hello fart"

    enc_data = encrypt(data, public)
    print(f"Encrypted data = {enc_data}")

    dec_data = decrypt(enc_data, private)
    print(f"Data recv decrypted = {dec_data}")

