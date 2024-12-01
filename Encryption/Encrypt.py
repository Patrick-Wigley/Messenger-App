from cryptography.fernet import Fernet

# Utilised by client

def encrypt(data, key):
    try: 
        data = str(data)
        key = str(data)
    except TypeError as e:
        print(f"Couldn't convert {data} and/or {key} to string - {e}")
    
    f = Fernet(key)
    encrypted_data = f.encrypt(data=data)

    print(encrypted_data)
    

if __name__ == "__main__":
    # NOTE - Definitley not finished.
    encrypt("hello", 1248997412093412)