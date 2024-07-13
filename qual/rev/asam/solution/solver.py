from ctypes import c_uint32 as d
from pwn import p32 as p, xor

FLAG = "hacktoday{TEA_in_wasm_but_iMade_easy_s0_uC0uld_cheese_it_but_1H0pe_you_n0t}"

# Solve TEA encryption

v = []
v.append(6597966560967363488)
v.append(17679903139760180007)
v.append(14198857734558046055)
v.append(14746339574093167844)
v.append(5568311295310460598)
v.append(16153832260982745162)
v.append(2093532499834777045)
v.append(13521399118574993695)
v.append(1232776455115851805)
v.append(5760351557880941997)
enc = [item for sublist in [(d(v[i]).value, d(v[i] >> 4 * 8).value) for i in range(len(v))][::-1]  for item in sublist]
key = [2037477999, 1903325039, 1919905641, 1869572462]

def decrypt(data):
    v0 = data[0]
    v1 = data[1]
    delta = 0x9E3779B9
    sum = d(delta << 5).value
    for i in range(32):
        v1 = d(v1 - (d(v0 << 4).value + key[2] ^ v0 + sum ^ (v0 >> 5) + key[3])).value
        v0 = d(v0 - (d(v1 << 4).value + key[0] ^ v1 + sum ^ (v1 >> 5) + key[1])).value
        sum = d(sum - delta).value
    return [v0, v1]

print(b"".join([p(i)+p(j) for i,j in [decrypt(enc[k:k+2]) for k in range(0, len(enc), 2)]]).strip(b'\x00').decode())

# Solve Cheese (easy)

from libnum import n2s

enc = b''
enc += n2s(5149)
enc += n2s(1493644828)
enc += n2s(436908589447717208)
enc += n2s(3899303686850805814)
enc += n2s(872022723546199565)
enc += n2s(368267306934360346)
enc += n2s(3895642299542408205)
enc += n2s(586594083881618230)
enc += n2s(295557651394658358)

print(xor(enc[::-1], 0x69))