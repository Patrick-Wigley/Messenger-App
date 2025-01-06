# Diffie-Hellman

import random

# B generator
B = 17 # g
# prime number - used GenPrime.bat
P = 5674072262951548623990802345966275946059526228370082500249898070096090705403871098241339970283678461754870405416417310979379922475322804164173458302758071195028963585128930251356825267202882245776819815571518358280999975977179857783027492657932472955165242032350745548008818741735197227387669863067433953110395220958756342206584268753045688751863807076799986827801929388514324058108972656119361793992770624321587749899336602656119038299963812650850885095301509258943888375524804438286440237927630867132786920972470985827812830359101815064467978755215112342633297920233180086708610274742584526704505765404119885009366135490709892990639656012633112190415685622458875880522957959012719718396082360275122456567847482372304615445779746632478310894097713895641865506066683181024755679096343060670378457395813631749877913629261041397399160070994141613719296597031735378785088837445056137431163745883074099543820938770983061791701671
NUM_BITS = 3072

def produce_private_key() -> int:
    return random.getrandbits(NUM_BITS)

def produce_public_key(private_key) -> int:
    """
    Param:
    private_key (Int)
    """
    return pow(B, private_key, P)

def get_process_pub(others_public_key, my_private_key) -> int:
    """
    Param:
    others_public_key (Int) - public key received from packet/frame transimssion
    my_private_key (Int) - Saved private key for this client
    Returns:
    int - If valid public key received, key will be correct thus data will decrypt sucessfully
    """
    return pow(others_public_key, my_private_key, P)


if __name__ == "__main__":
    # Alice and Bob example.

    alice_priv_k = produce_private_key() # a
    bob_priv = produce_private_key()     # b

    alice_pub_k = produce_public_key(alice_priv_k)      # Qa
    bob_pub_k = produce_public_key(bob_priv)            # Qb


    # AFTER TRANSIMISSION 
    # On Bobs side:
    bob_exchanged = get_process_pub(alice_pub_k, bob_priv)
    # On Alices side:
    alices_exchanged = get_process_pub(bob_pub_k, alice_priv_k)

    assert bob_exchanged == alices_exchanged
    print("Key exchange is valid" if bob_exchanged == alices_exchanged else "Key exchange is NOT valid")