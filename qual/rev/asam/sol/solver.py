from ctypes import c_uint32 as d
from pwn import p32 as p

FLAG = "hacktoday{teh_yang_asam_or_should_we_say_TEA_in_WASM??}"

v = [0]*7
v[0] = -6225995687070316293
v[1] = -4667559612723830560
v[2] =  8322962302255532578
v[3] =  1868868531417401368
v[4] = -8053092727678724853
v[5] =  2547027027142942705
v[6] =  5760351557880941997
enc = [item for sublist in [(d(v[i]).value, d(v[i] >> 4 * 8).value) for i in range(7)][::-1] for item in sublist]
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