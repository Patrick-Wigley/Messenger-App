


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
    return data # NOTE HASH THIS



if __name__ == "__main__":
    
    
    print(list_to_str_with_commas([1,2,3,4]))