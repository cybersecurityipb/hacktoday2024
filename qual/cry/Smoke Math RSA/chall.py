from Crypto.Util.number import *
from math import gcd
from flag import FLAG
import sys
import time

start_time = time.time()
sys.set_int_max_str_digits(0)

def methbit(dbit):
    a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20 = getRandomNBitInteger(dbit), getRandomNBitInteger(dbit), getRandomNBitInteger(dbit), getRandomNBitInteger(dbit), getRandomNBitInteger(dbit), getRandomNBitInteger(dbit), getRandomNBitInteger(dbit), getRandomNBitInteger(dbit), getRandomNBitInteger(dbit), getRandomNBitInteger(dbit), getRandomNBitInteger(dbit), getRandomNBitInteger(dbit), getRandomNBitInteger(dbit), getRandomNBitInteger(dbit), getRandomNBitInteger(dbit), getRandomNBitInteger(dbit), getRandomNBitInteger(dbit), getRandomNBitInteger(dbit), getRandomNBitInteger(dbit), getRandomNBitInteger(dbit)
    return(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20)

def meth_crack(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20):
    b1 = (a1 - 1) * (a2 - 1) * (a1 - a2)**2  
    b2 = ((a1 - a2) * (a2 - a1))**2 + a1 + a2
    b3 = (a3 - 1) * (a4 - 1) * (a3 - a4)**2
    b4 = ((a3 - a4) * (a4 - a3))**2 + a3 + a4
    b5 = (a5 - 1) * (a6 - 1) * (a5 - a6)**2
    b6 = ((a5 - a6) * (a6 - a5))**2 + a5 + a6
    b7 = (a7 - 1) * (a8 - 1) * (a7 - a8)**2
    b8 = ((a7 - a8) * (a8 - a7))**2 + a7 + a8
    b9 = (a9 - 1) * (a10 - 1) * (a9 - a10)**2
    b10 = ((a9 - a10) * (a10 - a9))**2 + a9 + a10
    b11 = (a11 - 1) * (a12 - 1) * (a11 - a12)**2
    b12 = ((a11 - a12) * (a12 - a11))**2 + a11 + a12
    b13 = (a13 - 1) * (a14 - 1) * (a13 - a14)**2
    b14 = ((a13 - a14) * (a14 - a13))**2 + a13 + a14
    b15 = (a15 - 1) * (a16 - 1) * (a15 - a16)**2
    b16 = ((a15 - a16) * (a16 - a15))**2 + a15 + a16
    b17 = (a17 - 1) * (a18 - 1) * (a17 - a18)**2  
    b18 = ((a17 - a18) * (a18 - a17))**2 + a17 + a18
    b19 = (a19 - 1) * (a20 - 1) * (a19 - a20)**2
    b20 = ((a19 - a20) * (a20 - a19))**2 + a19 + a20
    o1 = a1 * a2 + a3 * a4 + a5 * a6 + a7 * a8 +  a9 * a10 
    o2 = a11 * a12 + a13 * a14 + a15 * a16 + a17 * a18 + a19 * a20
    return(o1, o2, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15, b16, b17, b18, b19, b20)

def coke(nbit):
    while True:
        p = getRandomNBitInteger(nbit)
        q = getRandomNBitInteger(nbit)
        if isPrime(p) and  isPrime(q):
            phi = (p - 1) * (q - 1)
            n = p * q 
            e = int('0x10001', 16)
            if gcd(e, phi) == 1:
                dn = inverse(e, phi)
                dp = dn % (p - 1)
                return(e, n, dp)                        

def cigar(n, o1, o2):
    str_n = str(n)
    str_o1 = str(o1)
    str_o2 = str(o2)
    new_str = str_o2 + str_n + str_o1
    hehe = int(new_str)
    return(hehe)
    
def coke_enc(msg, pubkey):
    e, n = pubkey
    return pow(msg, e, n)

def smoke(FLAG, e, n):
    FLAG = int(FLAG.encode("utf-8").hex(), 16)
    cipher = coke_enc(FLAG, (e, n))
    return(cipher)


nbit, dbit = 1024, 256
a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20 = methbit(nbit)
o1, o2, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15, b16, b17, b18, b19, b20 = meth_crack(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20)
e, n, dp = coke(nbit)
hehe = cigar(n, o1, o2)
cipher = smoke(FLAG, e, n)

print('cipher =',"'", hex(cipher),"'")
print('hehe =',"'",hex(hehe),"'")
print('c1 =',"'",hex(b1),"'")
print('c2 =',"'",hex(b2),"'")
print('c3 =',"'",hex(b3),"'")
print('c4 =',"'",hex(b4),"'")
print('c5 =',"'",hex(b5),"'")
print('c6 =',"'",hex(b6),"'")
print('c7 =',"'",hex(b7),"'")
print('c8 =',"'",hex(b8),"'")
print('c8 =',"'",hex(b8),"'")
print('c9 =',"'",hex(b9),"'")
print('c10 =',"'",hex(b10),"'")
print('c11 =',"'",hex(b11),"'")
print('c12 =',"'",hex(b12),"'")
print('c13 =',"'",hex(b13),"'")
print('c14 =',"'",hex(b14),"'")
print('c15 =',"'",hex(b15),"'")
print('c16 =',"'",hex(b16),"'")
print('c17 =',"'",hex(b17),"'")
print('c18 =',"'",hex(b18),"'")
print('c19 =',"'",hex(b19),"'")
print('c20 =',"'",hex(b20),"'")
print('dp =',"'",hex(dp),"'")
print('chall execute time =',"--- %s seconds ---" % (time.time() - start_time))