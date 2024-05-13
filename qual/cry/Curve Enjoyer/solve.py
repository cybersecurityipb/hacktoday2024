from pwn import *
from sage.all import *
from Crypto.Util.number import *

r = process(["python3", "server.py"])

def send(bit):
    r.sendlineafter(b": ", str(bit).encode())
    p = r.recvline(0).split(b"= ")[-1].decode()
    P = r.recvline(0).split(b"= ")[-1].decode()
    Q = r.recvline(0).split(b"= ")[-1].decode()
    return int(p), eval(P), eval(Q)

mod = []
c = []

for i in range(50):
    print(i)
    p, P, Q, = send(30)
    a = ((P[1]**2-Q[1]**2)-(P[0]**3-(Q[0])**3))*pow(P[0]-(Q[0]),-1,p)%p
    b = -(P[0]**3+a*P[0]-P[1]**2)%p
    E = EllipticCurve(GF(p), [a, b])
    P = E(P)
    Q = E(Q)
    d = discrete_log(Q, P, P.order(), operation='+')
    assert P*d == Q
    mod.append(P.order())
    c.append(d)
    
print(long_to_bytes(crt(c,mod)))