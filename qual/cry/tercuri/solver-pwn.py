from pwn import *

from Crypto.Util.number import *
from sympy.ntheory.modular import crt
from gmpy2 import *
from itertools import combinations

pasangan = {}
stop = False

while True:
    conn = remote('194.238.16.121', 8020)
    if stop:
        break

    conn.recvuntil("n = ")
    n = int(conn.recvline().strip())
    conn.recvuntil("e = ")
    e = int(conn.recvline().strip())
    conn.recvuntil("c = ")
    c = int(conn.recvline().strip())

    #SOLVER
    if e == 17:
        if pasangan.get(e):
            pasangan[e].append((n,c))
        else:
            pasangan[e] = [(n,c)]
        
    for key in pasangan.keys():
        if len(pasangan[key]) >= 3:
            ns = [p[0] for p in pasangan[key]]
            cs = [p[1] for p in pasangan[key]]

            # Generate combinations of ns and cs
            ns_combinations = combinations(ns, 3)
            cs_combinations = combinations(cs, 3)

            for ns_comb, cs_comb in zip(ns_combinations, cs_combinations):
                me = crt(ns_comb, cs_comb)

                hasil = iroot(me[0], key)[0]
                try:
                    byteAns = long_to_bytes(hasil)
                    ans = byteAns.decode()
                    print("masuk")
                    print(ans)
                    print(f'jumlah = {len(pasangan[key])}')
                    stop = True
                    break  # Exit the loop once the flag is found
                except:
                    pass

    if stop == False:
        print(pasangan.keys())
        print(pasangan)
        print([len(pasangan[key]) for key in pasangan.keys()])

conn.close()