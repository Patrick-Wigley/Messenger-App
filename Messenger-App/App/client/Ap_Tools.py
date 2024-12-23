# def list_to_str_with_commas(list_) -> str:
#     if type(list_) is list or type(list_) is tuple:
#         ret = str(list_)
#         ret = ret[1:len(ret)-1]
#         return ret
#     else:
#         raise TypeError
    

# def pairing_function(x, y):
#     """ https://stackoverflow.com/questions/4226317/generate-a-unique-value-for-a-combination-of-two-numbers 
#         Tested this with some values and it's passed. 
#     """
#     ret =  y | (x << 32) if x > y else x | (y << 32)
#     return ret


# def extract_cmd(data) -> tuple:
#     """
#     Params:
#         data (str): #IC[command] (arg1, arg2, ...) 
#     Returns:
#         tuple: (cmd, args)
#     # """

#     cmd = data[data.find("[")+1 : data.find("]")]  
#     args_str = data[data.find("(")+1 : data.find(")")] 
#     # '_' Denotes a SPACE
#     # ' ' Will be removed
#     args = [arg.replace(" ", "").replace("_", " ") for arg in args_str.split(",")]
#     return (cmd, args)




if __name__ == "__main__":
    pass
