# Cyclic Redundancy Check - Learnt from https://www.geeksforgeeks.org/cyclic-redundancy-check-python/

input_str = "LIL"
data = (''.join(format(ord(x), 'b') for x in input_str))


"""
XOR Gate Reminder - Only true if ONLY ONE is ON
a | b |XOR
0 | 0 | 0
0 | 1 | 1
1 | 0 | 1
1 | 1 | 0 
"""

def XOR(a, b):
    ret_list = []

    # Linearly apply XOR to vars
    for i in range(0, len(a)):
        ret_list.append('0' if a[i] == b[i] else '1')
    return ''.join(ret_list)

def mod2div(divident, divisor):
    """ Divides the binary data by the key & stores the remainder"""
    len_divisor = len(divisor)
    tmp = divident[0:len_divisor]

    for i in divident:
        pass


def encode_data(data, key):
    # Performs Mod-2 Division

    key_len = len(key)
    # 
    data_with_keylen = None


if __name__ == "__main__":
    print(XOR("01010", "01100")) # FFTTF

