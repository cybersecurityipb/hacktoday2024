from Crypto.Util.number import bytes_to_long as b2l, long_to_bytes as l2b

def grey_v2(x):
    n = x ^ (x//2) ^ (x//4)
    return n

def grey_v2_reversed(x):
    x = bin(x)[2:]
    x = [int(i) for i in x]
    n = []
    n.append(x[0])
    n.append(x[1]^x[0])
    for i in range(len(x)-2):
        n.append(x[i+2]^n[i]^n[i+1])
    n = [str(i) for i in n]
    n = ''.join(n)
    return int(n, 2)

def grey_v3(x):
    n = (2*x) ^ (x) ^ (x//2) ^ (x//4)
    return n

def grey_v3_reversed(x):
    x = bin(x)[2:]
    x = [int(i) for i in x]
    n = []
    n.append(x[0])
    n.append(x[1]^n[0])
    n.append(x[2]^n[0]^n[1])
    for i in range(len(x)-4):
        n.append(x[i+3]^n[i]^n[i+1]^n[i+2])
    n = [str(i) for i in n]
    n = ''.join(n)
    return int(n, 2)

with open('file.txt', 'r') as file:
    ct = file.read()[3:]
    ct = str(int(ct))
print(ct)
    
flag = []
for i in range(1, len(ct)//2):
    n1 = ct[:(i+1)]
    n2 = ct[(i+1):]
    n1 = int(n1)
    n2 = int(n2)
    for _ in range(1000):
        n1 = grey_v2_reversed(n1)
    for _ in range(1000):
        n2 = grey_v3_reversed(n2)
    flag.append(l2b(n1)+l2b(n2))

substring = b'hacktoday'
flag_ = [i for i in flag if substring in i]
print(flag_)
