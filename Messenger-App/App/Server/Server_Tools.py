from hashlib import sha256


def list_to_str_with_commas(list_) -> str:
    if type(list_) is list or type(list_) is tuple:
        ret = str(list_)
        ret = ret[1:len(ret)-1]
        return ret
    else:
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


def hash_data(data) -> str:
    return sha256(data.encode("utf-8")).hexdigest() # NOTE HASH THIS

def caesar_cipher_value(data, encrypt):
    MAX = 122
    KEY = 9
    
    if isinstance(data, str):
        new_data = ""
        for char in data:
            new_data += chr((ord(char) + KEY) % MAX if encrypt else (ord(char) - KEY) % MAX)
        return new_data

    else:
        print(f"WE ARE RUNNING WITH A {type(data)} - Data is: {data}")
        raise TypeError


if __name__ == "__main__":
    encrypted = caesar_cipher_value("test", encrypt=True)
    decrypted = caesar_cipher_value(encrypted, encrypt=False)


    #print(list_to_str_with_commas([1,2,3,4]))