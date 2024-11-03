from typing import Union
import socket

def handle_recv(conn, addr) -> Union[tuple, None]:
    """ 
    Params:
        conn (Socket):
        addr (_RetAddress):
    Returns:
        tuple|None: 'cmd, args' On SUCCESSFUL Transmission 
    """
    try:
        data = conn.recv(1024).decode("utf-8") 
        return extract_cmd(data)
    except socket.error as e:
        print(f"[ERROR]: IN {handle_recv.__name__}\n{e}")
        return None

def handle_send(conn, addr, cmd, args=None) -> bool:
    try:
        send = f"#IC[{cmd}] ({list_to_str_with_commas(args)})"
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
        tuple: (cmd, args)
    # """
    cmd = data[data.find("[")+1 : data.find("]")]  
    args_str = data[data.find("(")+1 : data.find(")")] 
    args = [arg.replace(" ", "") for arg in args_str.split(",")]
    return (cmd, args)

def pairing_function(x, y):
    """ https://stackoverflow.com/questions/4226317/generate-a-unique-value-for-a-combination-of-two-numbers 
        Tested this with some values and it's passed. 
    """
    ret =  y | (x << 32) if x > y else x | (y << 32)
    return ret



if __name__ == "__main__":
    print(pairing_function(11, 4))
    print(pairing_function(4, 11))
    print(list_to_str_with_commas(['1','2','3','4']))