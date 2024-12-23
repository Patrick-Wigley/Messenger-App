from typing import Union
import socket
import hashlib
import os

# DATA TRANSMISSION 
def handle_recv(conn, addr) -> Union[tuple, None]:
    """ 
    Params:
        conn (Socket):
        addr (_RetAddress):
    Returns:
        tuple: ('cmd', (args' On SUCCESSFUL Transmission 

    """
    try:
        data = conn.recv(1024).decode("utf-8") 
        return extract_cmd(data)
    except socket.error as e:
        print(f"[ERROR]: IN {handle_recv.__name__}\n{e}")
        return None

def extract_args_from_list(args) -> str:
    return ''.join(args)

def handle_send(conn, addr, cmd=None, args=None, request_out=None) -> bool:
    """ 
    Takes command want to send & optionally any arguments
    Params:
        conn (Socket):
        addr (_RetAddress):
        cmd (String):
        ards (List): 
    """
    try:
        if not request_out:
            send = f"#IC[{cmd}] ({args})"       # send = f"#IC[{cmd}] ({list_to_str_with_commas(args)})"
        else:
            send = request_out
        print(f"SENDING: {send}")
        conn.send(send.encode("utf-8"))
        return True
    except socket.error as e:
        print(f"[ERROR]: IN {handle_send.__name__}\n{e}")
        return False


def list_to_str_with_commas(list_) -> str:
    if type(list_) is list or type(list_) is tuple:
        ret = str(list_).replace("'", "")
        ret = ret[1:len(ret)-1]
        return ret
    elif not list_:
        return ""
    else:
        print(f"[ERROR] Unexpected type: got {type(list_)} - {list_}")
        raise TypeError
    

def extract_cmd(data) -> tuple:
    """
    Params:
        data (str): #IC{command} (arg1, arg2, ...) 
    Returns:
        tuple|None (("cmd" ["arg1", "arg2"])): 
        
    # """
    cmd = data[data.find("[")+1 : data.find("]")]  
    
    last_closed_bracket_index = len(data)-(data[::-1].find(")"))-1
    args_tuple = data[data.find("(") : last_closed_bracket_index+1]
    
    args_evaluation = eval(args_tuple)
    print(f"Evalutaed string is: {args_evaluation} - type is {type(args_evaluation)}")
    
    if isinstance(args_evaluation, tuple):
        args = list(args_evaluation)
    elif not isinstance(args_evaluation, list):
        args = [args_evaluation]
    else:
        args = args_evaluation
    print(f"final args state: {args}")

    # args_str = data[data.find("(")+1 : last_closed_bracket_index] # snip out first ( and last ) in string

    # args = [arg.replace(" ", "") for arg in args_str.split(",")]

    return (cmd, args)


def check_md5():
    pass

# OTHER 

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