import KeyGen

def alices_side():
    priv_key = KeyGen.produce_private_key()
    public_key = KeyGen.produce_public_key(priv_key)
    return public_key # "Sends" key to Bob

if __name__ == "__main__":
    # Bobs side
    priv_key = KeyGen.produce_private_key()

    recv_alice_pub = alices_side() # Imagine/Pretend this is recv from Alice

    KeyGen.get_process_pub(recv_alice_pub, priv_key)