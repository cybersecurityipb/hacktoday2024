from pwn import *
import scipy.stats as st

berhasil = 1 - 2*st.norm.cdf(-0.42)
gagal = 1 - 2*st.norm.cdf(-2)

io = process(['python3', 'server.py'])

io.recvuntil(b'= ')
iv = bytes.fromhex(io.recvline(0).decode())

io.recvuntil(b'= ')
ct = bytes.fromhex(io.recvline(0).decode())

def oracle(ct):
    io.sendlineafter(b'ciphertext: ', ct.hex().encode())
    result = io.recvline(0)
    return b'HAHAHA' == result

def get_oracle(ct, n_try):
    result = [oracle(ct) for _ in range(n_try)]
    return sum(result) / n_try


ct = iv + ct
ct = [ct[i:i+16] for i in range(0, len(ct), 16)]

full_plain = b''
for k in range(1, len(ct)):
    plain = b''
    blok_kiri = ct[-(k+1)]
    blok_kanan = ct[-k]
    blok_akhir = b''
    for i in range(16):
        for j in range(256):
            iv_baru = b'\x00'*(15 - i) + bytes([j]) + blok_akhir
            send_ct = iv_baru + blok_kanan
            prob = get_oracle(send_ct, 20)
            if abs(prob - berhasil) < abs(prob - gagal):
                plain = xor(bytes([j]), i + 1, blok_kiri[-(i + 1)]) + plain
                blok_akhir = xor(blok_kiri[-(i + 1):], plain, i + 2)
                print(plain, prob, j)
                break
    full_plain = plain + full_plain

print(full_plain)
io.interactive()