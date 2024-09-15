from utils import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

private_key_ECDSA = getRandomNBitInteger(256)
private_key_AES = os.urandom(16)
FLAG = b'hacktoday{REDACTED}'

def encrypt_with_sign(pt):
    global signer
    cipher = AES.new(private_key_AES, AES.MODE_ECB)
    ct = cipher.encrypt(pad(pt, 16))
    signature = signer.sign(ct)
    return signature

def decrypt_with_verify(signature):
    global signer
    ct = bytes.fromhex(signature['msg'])
    if signer.verify(signature):
        cipher = AES.new(private_key_AES, AES.MODE_ECB)
        try:
            pt = unpad(cipher.decrypt(ct), 16).decode()
        except Exception as e:
            return 'Hack Detected', False
        return pt, True 
    return 'Hack Detected', False

def displayMenu():
    print("1. Get Token\n2. Get Flag\n3. Exit")

def main():
    global signer
    signer = ECDSA(private_key_ECDSA)
    print("Welcome to Fufufafa machine, Choose the services:")
    while True:
        displayMenu()
        try:
            choice = int(input('> '))
            if choice == 1:
                name = input('name: ')
                while name == 'Fufufafa':
                    name = input('name: ')
                signature = encrypt_with_sign(name.encode())
                print(f"signature = {signature}")
            elif choice == 2:
                signature = json.loads(input('give me your signature in JSON format: '))
                name, res = decrypt_with_verify(signature)
                if res:
                    if name == 'Fufufafa':
                        print(FLAG.decode())
                    else:
                        print(f'Hello {name}')
                else:
                    print("Ga valid signaturenya pls...")
            elif choice == 3:
                exit()
            else:
                pass
        except Exception as e:
            print("Error Occured...")





if __name__ == "__main__":
    main()