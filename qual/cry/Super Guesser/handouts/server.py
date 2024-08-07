from Crypto.Util.Padding import *
from Crypto.Cipher import AES
import os, random, numpy as np


iv = os.urandom(16)
key = os.urandom(16)
flag = b'hacktoday{REDACTED}'
mu, sd = np.random.uniform(-4269, 4269), np.random.uniform(1e-6, 2e-6)


def probabilistic_checker(inp):
    iv, ct = inp[:16], inp[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    result = cipher.decrypt(ct)
    trash = (mu - 0.42*sd) < np.random.normal(mu, sd) < (mu + 0.42*sd)
    try:
        unpad(result, 16)
    except Exception as e:
        trash =  (mu - 2*sd) < np.random.normal(mu, sd) < (mu + 2*sd)
    return trash

def main():
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(flag, 16))
    print(f"iv = {iv.hex()}")
    print(f"ct = {ct.hex()}")
    while True:
        try:
            inp = bytes.fromhex(input("Let me check your ciphertext: "))
            if probabilistic_checker(inp):
                print('HAHAHA')
            else:
                print('HEHEHE')
        except Exception as e:
            exit(-1)   
    
if __name__ == "__main__":
    main()