from Crypto.Util.Padding import *
from Crypto.Cipher import AES
import os, random, numpy as np


iv = os.urandom(16)
key = os.urandom(16)
flag = b'hacktoday{congrats_you_can_distinguish_the_oracleeeeeee}'
mu, sd = np.random.uniform(-4269, 4269), np.random.uniform(1e-6, 2e-6)
C1 = 0.80
C2 = 0.55


def probabilistic_checker(inp):
    iv, ct = inp[:16], inp[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    result = cipher.decrypt(ct)
    trash = (mu - C1*sd) < np.random.normal(mu, sd) < (mu + C1*sd)
    try:
        unpad(result, 16)
    except Exception as e:
        trash =  (mu - C2*sd) < np.random.normal(mu, sd) < (mu + C2*sd)
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