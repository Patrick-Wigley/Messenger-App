from typing import Union
import socket
import sys
from Shared.Encryption.Encrypt import (encrypt, decrypt, get_pub_priv_key, convert_to_key_from_pkcs)

DEBUG = False
ENCODE_FORMAT = "utf-8"

# DATA TRANSMISSION 
def handle_recv(conn, addr, recv_amount=1024, priv_key="", verbose=False, decrypt_data=True) -> Union[tuple, None]:
    """ 
    Params:
        conn (Socket):
        addr (_RetAddress):
    Returns:
        tuple: ('cmd', (args' On SUCCESSFUL Transmission 
    """
    
    try:
        # RECEIVING
        received_data = conn.recv(recv_amount)

        # DECRYPTING &&/|| DECODING TO STRING
        if decrypt_data:
            data_ready_to_use = decrypt(received_data, priv_key).decode(ENCODE_FORMAT)
            if verbose:
                print(f"Encrypted data received = {received_data} \Decrypted data = {data_ready_to_use}")
        else:
            # Not Decrypting
            data_ready_to_use = received_data.decode(ENCODE_FORMAT)

        
        # EXTRACTING COMMANDS & RETURNING
        return extract_cmd(data_ready_to_use)
    
    except socket.error as e:
        print(f"[ERROR]: IN {handle_recv.__name__}\n{e}")
        return None





def handle_send(conn, addr=None, cmd=None, args=None, request_out="", verbose=False, pub_key="", encrypt_data=True) -> bool:
    """ 
    Takes command want to send & optionally any arguments
    Params:
        conn (Socket):
        addr (_RetAddress):
        cmd (String):
        ards (List): 
    """
    try:

        # FORMATTING
        if not request_out:
            data = f"#IC[{cmd}] ({args})"
        else:
            data = request_out
        
        # Data segmenting:
        data_size = sys.getsizeof(data.encode(ENCODE_FORMAT))
        if data_size > 1024:
            pass

        # DEBUGING
        if verbose:
            print(f"Sending: {data}")

        # ENCODING
        data_encoded = data.encode(ENCODE_FORMAT)

        # ENCRYPTING
        if encrypt_data and pub_key:
            data_ready_to_send = encrypt(data_encoded, pub_key)
            if verbose:
                print(f"Sending As Encrypted: {data_ready_to_send}")
        else:
            # Not encrypting
            data_ready_to_send = data_encoded

        # SENDING
        conn.send(data_ready_to_send)
        return True
    
    except socket.error as e:
        print(f"[ERROR]: IN {handle_send.__name__}\n{e}")
        return False



    

def extract_cmd(data: str) -> tuple:
    """
    Params:
        data (str): "#IC[command] (arg1, arg2, ...)"
    Returns:
        tuple|None (("cmd" ["arg1", "arg2"])): 
        
    # """

    # COMMAND
    cmd = data[data.find("[")+1 : data.find("]")]  
    
    # ARGUMENTS
    last_closed_bracket_index = len(data)-(data[::-1].find(")"))-1
    args_tuple = data[data.find("(") : last_closed_bracket_index+1] # Extracts: (arg1, arg2, ...)

    args_evaluation = eval(args_tuple)
    if DEBUG:
        print(f"Evaluated string is: {args_evaluation} - type is {type(args_evaluation)}")
    
    # Stores arguments in LIST 
    if isinstance(args_evaluation, tuple):
        args = list(args_evaluation)
    elif not isinstance(args_evaluation, list):
        args = [args_evaluation]
    else:
        args = args_evaluation

    if DEBUG:
        print(f"final args state: {args}")

    return (cmd, args)


def check_md5():
    pass




def gen_keys():
    return get_pub_priv_key()

def convert_to_pkcs(pub):
    pub_pkcs = pub.save_pkcs1("DER")
    return pub_pkcs
def convert_from_pkcs(pub_pkcs: str):
    return convert_to_key_from_pkcs(pub_pkcs)

def handle_pubkey_share(conn, addr, sessions_generated_public_key, bi_directional_share=True, verbose=False):
    others_public_key = ""

    sent_key_to_client = False
    if bi_directional_share:
        sent_key_to_client = True
    got_key_from_client = False

    handle_send(conn, addr, cmd="RequestingPubKey", encrypt_data=False)

    while True:
        if not sent_key_to_client or not got_key_from_client:
            result = handle_recv(conn, addr, decrypt_data=False)
        
            if result:
                cmd, args = result
                if cmd == "SendingPubKey":
                    got_key_from_client = True
                    clients_public_key_pkcs = args[0]
                    others_public_key = convert_from_pkcs(clients_public_key_pkcs)
                    if verbose:
                        print(f"Got other participants public key - {others_public_key}")

                elif cmd == "RequestingPubKey":
                    sent_key_to_client = True
                    # Save key into pkcs for loading on client side
                    handle_send(conn, addr, cmd="SendingPubKey", args=convert_to_pkcs(sessions_generated_public_key))
                    if verbose:
                        print(f"Sending Public key to other participant - {sessions_generated_public_key}")


                else:
                    print(f"[{handle_pubkey_share.__name__}] GOT SOMETHING UNEXPECTED - {result}")
        else:
            # The key sharing session is SUCCESSFULLY finished
            return others_public_key





def send_request_for_pub_key(conn) -> str:
    #conn.send("#IC[GetPubKey]()".encode(ENCODE_FORMAT))
    handle_send(conn, cmd="GetPubKey", encrypt_data=False)

    data_recv = handle_recv(conn, )
    conn.recv(1024).encode(ENCODE_FORMAT)
    if "GetPubKey" in data_recv:
        return extract_cmd(data_recv)
    else:
        print("ERROR GETTING PUBLIC KEY")






# #####~~~~#####~~~~#####~~~~##### OTHER - Not used #####~~~~#####~~~~#####~~~~#####




def pairing_function(x, y):
    """
    Create a highly unique value using the two ids of 
    x = Client making call 
    y = Client receiving call 
    https://stackoverflow.com/questions/4226317/generate-a-unique-value-for-a-combination-of-two-numbers 
        Tested this with some values and it's passed. 
    """
    ret =  y | (x << 32) if x > y else x | (y << 32)
    return ret



if __name__ == "__main__":
    print(f"#~#~ RUNNING FILE {__file__} - Test all shared functions here ~#~# \n\n")
   
    
    print(extract_cmd("#IC[Something]((1,2), 11)"))


    if False:
        pair_one = (100, 4)
        pair_two = (99,4)

        # Tests if pairing either way returns same value
        assert (pairing_function(pair_one[0], pair_one[1])) == (pairing_function(pair_one[1], pair_one[0]))
        # Tests if two different pairs have unique values
        assert (pairing_function(pair_one[0], pair_one[1])) != (pairing_function(pair_two[0], pair_two[1]))

    
    #print(pairing_function(100, 4))
    #print(pairing_function(4, 100))
   
    #print(list_to_str_with_commas(['1','2','3','4']))

    #def extract_args_from_list(args) -> str:
#     return ''.join(args)









# def list_to_str_with_commas(list_: list|tuple) -> str:
#     if type(list_) is list or type(list_) is tuple:
#         ret = str(list_).replace("'", "")
#         ret = ret[1:len(ret)-1]
#         return ret
#     elif not list_:
#         return ""
#     else:
#         print(f"[ERROR] Unexpected type: got {type(list_)} - {list_}")
#         raise TypeError