section .text
    global _start

a:
    pop rbx
    pop rsp
    pop rdi
    pop rdx
    pop rsi
    pop rcx
    jmp [rsi - 37]

b:
    add rdx, rcx
    jmp [rdx- 69]

c: 
    nop
    nop
    jmp [rcx- 0x11]

d:
    add eax, edi
    jmp [rcx]

e:
    pop rbx
    jmp [rcx + 0x47]

f: 
    jmp [rsp - 100]

g: 
    xor rdx, rdx
    add rcx, rax
    xor rbx, rcx
    jmp rbx

h: 
    add rcx, [rsp + 0x18]
    jmp [rdx - 0x1d]

i:
    sub rsi, rbx
    jmp [rcx]

j: 
    xchg rdi, rsi
    fwait
    sub rax, rcx
    jmp [rdi + 11]

k:
    mul bl
    nop
    stc
    xchg rdx, rcx
    jmp [rcx]

_start:
    push rsp
    mov dx, 8
    inc dil
    mov rsi, rsp
    inc ax
    nop
    syscall

    xor rax, rax
    dec dil
    sub rsi, 99
    mov rdx, 115
    syscall

    jmp [rsp]