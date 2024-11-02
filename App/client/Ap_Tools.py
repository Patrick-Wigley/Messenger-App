
def pairing_function(x, y):
    """ https://stackoverflow.com/questions/4226317/generate-a-unique-value-for-a-combination-of-two-numbers 
        Tested this with some values and it's passed. 
    """
    ret =  y | (x << 32) if x > y else x | (y << 32)
    return ret


def extract_cmd(data) -> tuple:
    """ #IC{command} (arg1, arg2, ...) """

    cmd = data[data.find("[")+1 : data.find("]")]  
    args_str = data[data.find("(")+1 : data.find(")")] 
    # '_' Denotes a SPACE
    # ' ' Will be removed
    args = [arg.replace(" ", "").replace("_", " ") for arg in args_str.split(",")]
    return (cmd, args)


if __name__ == "__main__":
    print(pairing_function(11, 4))
    print(pairing_function(4, 11))

