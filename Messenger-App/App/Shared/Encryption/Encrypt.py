import rsa
import rsa.key


from Shared.Encryption.KeyGen import (produce_private_key,
                     produce_public_key,
                       get_process_pub)



def encrypt(data: bytes, pub_key: rsa.PublicKey) -> bytes:
    if isinstance(data, bytes):
        encrypted_data = rsa.encrypt(data, pub_key)
    else:
        raise TypeError # data EXPECTS TYPE bytes
    return encrypted_data

def decrypt(data: bytes, priv_key: rsa.PrivateKey) -> bytes: 
    decrypted_data = rsa.decrypt(data, priv_key)
    return decrypted_data

def get_pub_priv_key() -> None:
    return rsa.newkeys(2048)

def convert_to_key_from_pkcs(pub_pkcs: str) -> rsa.PublicKey:
    try:
        pub = rsa.key.PublicKey.load_pkcs1(pub_pkcs, format="DER")
    except rsa.VerificationError as e:
        print(f"ERROR CONVERTING TO PUBLIC KEY INSTANCE FROM PKCS: \n [VerificationError]: {e}")
    
    return pub





if __name__ == "__main__":
    # NOTE OLD METHOD:

    # Generate keys
    # private = produce_private_key()
    # public = produce_public_key(private)

    public, private = get_pub_priv_key()

    print(f"KEYS:\nPrivate Key = {private}\nPublic Key = {public}\n####")
    #### Would send the private key ONCE to client

    # Encrypt data
    data = "hello Messenger Application!"

    enc_data = encrypt(data, public)
    print(f"Encrypted data = {enc_data}")

    dec_data = decrypt(enc_data, private)
    print(f"Data recv decrypted = {dec_data}")

