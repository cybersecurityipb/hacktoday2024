from Crypto.Util.Padding import *
from Crypto.Cipher import AES
import os, random, numpy as np


iv = os.urandom(16)
key = os.urandom(16)
flag = b'hacktoday{random_process_so_cool___123__a4e63bcacf6c172ad84f9f4523c8f1acaf33676fa76d3258c67b7e7bbf16d777____24400004dc6ef1610dec22ebe2eb7159adf23bd154cbc7e30c30c9db0aa37868}'
mu, sd = np.random.uniform(-4269, 4269), np.random.uniform(1e-6, 2e-6)
C1, C2, C3, C4 = [np.random.uniform(0, 4) for _ in range(4)]


def probabilistic_checker(inp):
    iv, ct = inp[:16], inp[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    result = cipher.decrypt(ct)
    trash = (mu - C1*sd) < np.random.normal(mu, sd) < (mu + C2*sd)
    try:
        unpad(result, 16)
    except Exception as e:
        trash =  (mu - C3*sd) < np.random.normal(mu, sd) < (mu + C4*sd)
    return trash

def main():
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(flag, 16))
    print(f"iv = {iv.hex()}")
    print(f"ct = {ct.hex()}")
    print(f"{C1 = }")
    print(f"{C2 = }")
    print(f"{C3 = }")
    print(f"{C4 = }")
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