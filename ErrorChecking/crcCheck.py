# Cyclic Redundancy Check - Learnt from https://www.geeksforgeeks.org/cyclic-redundancy-check-python/

input_str = "LIL"
data = (''.join(format(ord(x), 'b') for x in input_str))
key = "1001"


def XOR(a, b):
    """
    XOR Gate Reminder - Only true if ONLY ONE is ON
    a | b |XOR
    0 | 0 | 0
    0 | 1 | 1
    1 | 0 | 1
    1 | 1 | 0 
    """
    ret_list = []

    # Linearly apply XOR to vars
    for i in range(0, len(a)):
        ret_list.append('0' if a[i] == b[i] else '1') # 1 if two values are NOT same; 0 if two values are same 
    return ''.join(ret_list)


def mod2div(dividend, divisor):
    """ 
    Params
        - dividend = The BinaryDataString
        - divisor = The Key

    Divides the binary data by the key & stores the remainder
        - Goes through string chunk by chunk 
    """
    
    # Length of key
    chunk_len = len(divisor)
    # Taking chunk of dividend (binary_data_str) for each step/iteration
    tmp = dividend[0:chunk_len]

    if len(dividend) % 2 != 0:
        print(f"Not segmented correctly?  dividend:{dividend} len:{len(dividend)} First-Chunk:{tmp}")
        raise TypeError

    while chunk_len < len(dividend):
        if tmp[0] == '1':
            tmp = XOR(divisor, tmp) + dividend[chunk_len]
        else:
            tmp = XOR('0'*chunk_len, tmp) + dividend[chunk_len]        
        chunk_len += 1
        
    # XOR Final bit
    if tmp[0] == '1':
        tmp = XOR(divisor, tmp)
    else:
        tmp = XOR('0'*chunk_len, tmp)

    checkedword = tmp
    return checkedword


def encode_data(data, key):
    key_len = len(key)
    # Adds (n-1 0's) to end of data_str
    data_with_key_len_zeros_at_end = data + ('0'*(key_len-1))
    # Performs Mod-2 Division
    remainder = mod2div(data_with_key_len_zeros_at_end, key)

    codedword = data + " " + remainder
    return codedword


if __name__ == "__main__":
    #print(''.join(format(ord(i), 'b') + " " for i in input_str))

    # Test it here
    print(encode_data(data, key))

#    print(XOR("01010", "01100")) # FFTTF

