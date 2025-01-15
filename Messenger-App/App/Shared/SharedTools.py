from typing import Union, Any
import socket
import sys
import math
import smtplib
from email.mime.text import MIMEText

from Shared.Encryption.Encrypt import (encrypt, decrypt, get_pub_priv_key, convert_to_key_from_pkcs)
from rsa import DecryptionError

# CONSTANTS
DEBUG = False
ENCODE_FORMAT = "utf-8"
SEGMENT_CHUNK_SIZE = 214 # Bytes
RECEIVE_AMOUNT = 214

# IC - CMDS
class CMD:
    """ CONSTANTS - ICs """

    # SEGMENTATION Commands
    SEGCOUNT = "SegCount" # Count of Segments going to be transmitted
    SEGLEN = "SegLen" # Length of a Segment (Used during encryption block transmissions)

    # AUTHENTICATION Commands
    LOGIN = "login"
    REGISTER = "register"

    # REQUEST OUTS Commands 
    CALLPERSON = "CallPerson"
    REFRESHCHATS = "RefreshChats"
    SEARCHCONTACT = "SearchContact"
    SAVECONTACT = "SaveContact"
    GETSAVECONTACTCHATS = "GetSavedContactsChats"
    GETMESSAGEHISTORY = "GetMessagesHistory"
    SENDMESSAGE = "SendMessage"
    UPDATE_CHAT_LOG_LIVE = "UpdateChatLogLive"
    EXIT = "exit"


    REQUEST_OUT_CMDS = [
        CALLPERSON,
        REFRESHCHATS, 
        SEARCHCONTACT,
        SAVECONTACT,
        GETSAVECONTACTCHATS,
        GETMESSAGEHISTORY,
        SENDMESSAGE,
    ]

    # SERVER-SPECIFIC Commands
    LIVECHAT = "LiveChat"
    BROADCAST = "BroadCast"
    BROADCAST_NOT_ALLOWED = "BroadCastNotAllowed"
    SERVER_SPECIFIC = [
        LIVECHAT,
        BROADCAST      
    ]



################################

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
        seg_count = None
        seg_count_data = conn.recv(RECEIVE_AMOUNT).decode("utf-8")
        if CMD.SEGCOUNT in seg_count_data:
            #print(f"GOT SEG COUNT DATA: {seg_count_data}")
            _, args = extract_cmd(seg_count_data)
            seg_count = args[0]
            if verbose:
                print(f"SEG COUNT EXPECTING IS: {seg_count}")

        else:
            print("SOMETHING WENT WRONG!!")

        try:
            chunks_concatenated = ""
            for _ in range(seg_count):
                seg_len_data = conn.recv(RECEIVE_AMOUNT).decode("utf-8")
                if CMD.SEGLEN in seg_len_data:
                    _, args = extract_cmd(seg_len_data)
                    receive_amount = args[0]
                else:
                    print("SOMETHING WENT WRONG")

                # RECEIVING data
                received_data = conn.recv(receive_amount)


                # DECRYPTING &&/|| DECODING TO STRING
                if decrypt_data:
                    data_chunk = decrypt(received_data, priv_key).decode(ENCODE_FORMAT)
                    if verbose:
                        print(f"Encrypted data received = {received_data} \nDecrypted data = {data_chunk}")
                else:
                    # Not Decrypting
                    data_chunk = received_data.decode(ENCODE_FORMAT)


                chunk_id, chunk_size, chunks_actual_data  = extract_segment_data(data_chunk)
                if verbose:
                    print(f"[DEBUG - SEGMENTING]: \n[ChunkID]: {chunk_id} & [ChunkSize]: {chunk_size} \n {chunks_actual_data} ")

                chunks_concatenated += chunks_actual_data


            if decrypt_data and verbose:
                print(f"Decrypted following: {chunks_concatenated}")


            # EXTRACTING COMMANDS & RETURNING
            return extract_cmd(chunks_concatenated)
        except DecryptionError as _:
            print(f"[Decryption was not complete]: IN {handle_recv.__name__}")
            return None

    except socket.error as _:
        print(f"[ABRUPT DISCONNECTION]: IN {handle_recv.__name__}")
        return None


def handle_send(conn, addr=None, cmd=None, args=None, request_out="", verbose=False, pub_key="", encrypt_data=True) -> bool:
    """ 
    Takes command to send & optionally any arguments
    Params:
        conn (Socket):
        addr (_RetAddress):
        cmd (String):
        ards (List): 
    """
    try:
        # FORMATTING
        if not request_out:
            data = format_ic_cmd(cmd=cmd, args=args)
            
        else:
            data = request_out
        

        data_len = len(data)
        seg_len = 50
        seg_count = math.ceil(data_len / seg_len) 

        # PRE-SHARE DATA SEGMENT COUNT
        conn.send(setup_chunk_to_send(format_ic_cmd(cmd=CMD.SEGCOUNT, args=seg_count).encode("utf-8")))

        # DEBUGING
        if verbose:
            print(f"Sending: {data}")

        encrypted_chunks = []
        for segment_id in range(seg_count):
            
            segment = get_segment(segment_id, data, segment_len=seg_len)
            #print(f"segment: {segment}")

            # ENCODING
            data_encoded = segment.encode(ENCODE_FORMAT)


            # ENCRYPTING
            if encrypt_data and pub_key:
                data_ready_to_send = encrypt(data_encoded, pub_key)
                if verbose:
                    print(f"Segment As Encrypted: {data_ready_to_send}")
                encrypted_chunks.append(data_ready_to_send)
            else:
                # Not encrypting
                data_ready_to_send = data_encoded

            # SENDING
            conn.send(setup_chunk_to_send(format_ic_cmd(cmd=CMD.SEGLEN, args=len(data_ready_to_send)).encode("utf-8")))
            conn.send(data_ready_to_send)
        
        if verbose:
            print(f"#~#~ TRANSMITTING CMD = '{cmd}'~#~# \n Segments transmitted: {seg_count}\n Segment Len: {seg_len}\n\n Data Transmitted: {data} \n\n Data Encrypted (Actual Data Sent): {encrypted_chunks}\n\n")
        return True
    
    except socket.error as e:
        print(f"[ABRUPT DISCONNECTION]: IN {handle_send.__name__}\n{e}")
        return False 

def setup_chunk_to_send(data: bytes) -> bytes:
    #RECEIVE_AMOUNT = 1024
    data_in_fixed_chunk = data + ((RECEIVE_AMOUNT - len(data)) * b' ')
    return data_in_fixed_chunk

def format_ic_cmd(cmd: str, args: Any = None) -> str:
    return f"#IC[{cmd}] ({args})"


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


def extract_segment_data(chunk: str) -> tuple:
    chunk_info = chunk[chunk.find("<")+1 : chunk.find(">")]
    chunk_id, chunk_size = chunk_info.replace(" ", "").split(",")
    
    chunk_data = chunk[chunk.find(">")+1 :]
    chunks_actual_data = chunk_data[: int(chunk_size)]        # Removes extra empty data - which is used to make the chunk a fixed size 

    #print(f"chunk_id: {chunk_id}, chunk_size: {chunk_size}")
    #print(f"chunk_info: {chunks_actual_data}")

    return (chunk_id, chunk_size, chunks_actual_data)


################################



# KEY & ENCRYPTION HANDLING 
def gen_keys():
    return get_pub_priv_key()

def convert_to_pkcs(pub):
    pub_pkcs = pub.save_pkcs1("DER")
    return pub_pkcs
def convert_from_pkcs(pub_pkcs: str):
    return convert_to_key_from_pkcs(pub_pkcs)

def handle_pubkey_share(conn, addr, sessions_generated_public_key, bi_directional_share=True, verbose=False):
    others_public_key = None

    sent_key_to_client = False
    if bi_directional_share:
        sent_key_to_client = True
    got_key_from_client = False


   
    send_result = handle_send(conn, addr, cmd="RequestingPubKey", encrypt_data=False)
    if send_result:
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
                        send_result = handle_send(conn, addr, cmd="SendingPubKey", args=convert_to_pkcs(sessions_generated_public_key))
                        if verbose:
                            print(f"Sending Public key to other participant - {sessions_generated_public_key}")
                        if not send_result:
                            return None

                    else:
                        print(f"[{handle_pubkey_share.__name__}] GOT SOMETHING UNEXPECTED - {result}")
                else:
                    return None
            else:
                # The key sharing session is SUCCESSFULLY finished
                return others_public_key
    else:
        return None

################################

# FRAME/PACKET SEGMENTING 
def segment_str(msg: str) -> list:
    """ Each segment is prefixed with CHUNK NUMBER - 
    Notation is <Segmented ID>[Login](arg1, arg2)  - SPLITS STRING WITHOUT CONSIDERATION OF WHAT DATA IS BEING SPLIT e.g. '<1>[Logou' '<2>t](arg)' is possible
    """
    msg_len = len(msg.encode("utf-8"))
    chunks_count = math.ceil(msg_len / SEGMENT_CHUNK_SIZE) 

    ret = []
    pivot = 1
    for chunk_index in range(chunks_count):
        data_chunk = msg[SEGMENT_CHUNK_SIZE*(pivot-1) : SEGMENT_CHUNK_SIZE*pivot]
        ret.append(f"<{chunk_index}, {len(data_chunk)}>{data_chunk}")
        pivot += 1

    return ret

def get_segment(seg_id, data:str, segment_len:int):
    data_chunk = data[segment_len*(seg_id) : segment_len*(seg_id+1)]
    #print(f"Data: {data}; \n\nSegment: {data_chunk}")
    return f"<{seg_id}, {len(data_chunk)}>{data_chunk}"


################################

# ERROR CHECKING
def check_md5():
    pass

# EMAILING

def send_email(receiver_email, data, subject):
    print(f"SENDING EMAIL TO: {receiver_email} \nMESSAGE BEING SENT: {data}")
    sender_email = "uodmessengerapp@gmail.com"
    password = "yunj jscm rgdu xuad" # Settings Password: 'Derby100715281' - App Password: 'yunj jscm rgdu xuad'
    msg = MIMEText(data, "plain")
    msg["Subject"] = subject


    host_name = "smtp.gmail.com"
    with smtplib.SMTP_SSL(host_name) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()



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



#def send_request_for_pub_key(conn) -> str:
#     #conn.send("#IC[GetPubKey]()".encode(ENCODE_FORMAT))
#     handle_send(conn, cmd="GetPubKey", encrypt_data=False)

#     data_recv = handle_recv(conn, )
#     conn.recv(1024).encode(ENCODE_FORMAT)
#     if "GetPubKey" in data_recv:
#         return extract_cmd(data_recv)
#     else:
#         print("ERROR GETTING PUBLIC KEY")






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