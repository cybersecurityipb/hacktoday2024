from Crypto.Cipher import ChaCha20
from Crypto.Util.number import bytes_to_long, long_to_bytes

# dotnet publish -r win-x64 -c Release -p:PublishAot=true

with open('flag.txt.Encrypted', 'rb') as f:
    data = f.read()

n = 167779367812792709915032707913032638382146251004558791142676786028501280044057627112826094280092505414510766384827088804978848108688648026981142540400168610823829003843442596437735093142183606826724002523744218048425313679193864739770021775952653310093258321014896182483000543295733022993925140727306455407233
phi = n -1
d = pow(0x10001, -1, phi)

length = n.bit_length()//8 # - 1
encnonce = data[-length-1:][::-1]
nonce = long_to_bytes(pow(bytes_to_long(encnonce),d,n))
key = data[-length-32-1:-length-1]
# print(key, nonce)
print(ChaCha20.new(key=key, nonce=nonce).decrypt(data[:-length-32-1]).decode())