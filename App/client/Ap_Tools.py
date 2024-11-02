
def pairing_function(x, y):
    """ https://stackoverflow.com/questions/4226317/generate-a-unique-value-for-a-combination-of-two-numbers 
        Tested this with some values and it's passed. 
    """
    ret =  y | (x << 32) if x > y else x | (y << 32)
    return ret



if __name__ == "__main__":
    print(pairing_function(11, 4))
    print(pairing_function(4, 11))

