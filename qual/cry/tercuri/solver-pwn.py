from pwn import *

from Crypto.Util.number import *
from sympy.ntheory.modular import crt
from gmpy2 import *
from itertools import combinations

pasangan = []
stop = False

while True:
    conn = remote('localhost', 8020)
    if stop:
        break

    conn.recvuntil(b"n = ")
    n = int(conn.recvline().strip())
    conn.recvuntil(b"e = ")
    e = int(conn.recvline().strip())
    conn.recvuntil(b"c = ")
    c = int(conn.recvline().strip())

    if e == 17:
        pasangan.append((n, c))
        
    if len(pasangan) >= 19:

        comb = combinations(pasangan, 7)

        for c in comb:
            ns = [n for n, _ in c]
            cs = [c for _, c in c]

            me = crt(ns, cs)

            hasil = iroot(me[0], 17)[0]
            try:
                byteAns = long_to_bytes(hasil)
                ans = byteAns.decode()
                print(ans)
                print(f'jumlah = {len(pasangan)}')
                if 'hacktoday' in ans:
                    stop = True
                    print(ans)
                    break
            except:
                pass
        pasangan = []

    if not stop:
        print(len(pasangan))

conn.close()