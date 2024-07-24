from Crypto.Util.number import *
from math import gcd
from flag import FLAG


def keybit(nbit, dbit):
    assert 2*dbit < nbit
    while True :
        a, b, c = getRandomNBitInteger(nbit // 2 - dbit), getRandomNBitInteger(nbit // 2 - dbit), getRandomNBitInteger(nbit // 2 - dbit)
        x = a * b + c
        y = a * c + b
        z = a + b + c 
        p = b * b + a 
        q = c * c + a 
        if isPrime(p) and  isPrime(q):
                phi = (p - 1) * (q - 1)
                n1 = p * q 
                e = getRandomNBitInteger(dbit)
                if gcd(e, phi) == 1:
                        d = inverse(e, phi)
                        return(e, n1, x, y, z)
                        
                    
def encrypt(msg, pubkey):
    e, n = pubkey
    return pow(msg, e, n)

nbit, dbit = 1024, 256

e, n1, x, y, z = keybit(nbit, dbit)

FLAG = int(FLAG.encode("utf-8").hex(), 16)

cipher = encrypt(FLAG, (e, n1))

print('e =', e)
print('cipher =', cipher)
print('x =', x)
print('y =', y)
print('z =', z)


