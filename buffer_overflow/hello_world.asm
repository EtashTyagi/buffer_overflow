; x86_64 assembly Hello World Program
; x86-64 syscall:
;	1.	rax -> syscall
;	2.	rax -> return value
;	3.	rdx -> return value 2
;	4.	rdi, rsi, rdx, r10, r8, r9 -> arguments
; Called using 'syscall' command
; Etash Tyagi

global _start

section .text
_start:						; Jump call exec method for shellcode
	jmp	shellcode_caller		; Jump to shellcode_caller

shellcode:
	pop	rsi				; rsi = Hello world string stack pointer
	
	xor	rax, rax			; rax = 0
	add	rax, SYS_WRITE			; rax = SYS_WRITE

	xor	rdi, rdi			; rdi = 0
	add	rdi, STDOUT			; rdi = STDOUT

	xor	rdx, rdx			; rdx = 0
	add	rdx, MSG_LEN			; rdx = message length
	syscall					; write hello world to STDOUT

	xor 	rax, rax			; rax = 0
	add	rax, SYS_EXIT			; rax = SYS_EXIT

	xor	rdi, rdi			; rdi = 0 [EXIT_SUCCESS]
	syscall					; Graceful exit


shellcode_caller:				; call the 'shellcode', pass string in stack
	call 	shellcode
	message: db "Hello World!", 10 ; message

; Utility data, only constant data must be passed into shellcode
section .data
 	message_:		db "Hello World!", 10
 	MSG_LEN:		equ $-message_	; message_length
 	SYS_WRITE:		equ 1		; write systemcall code
 	STDOUT:			equ 1		; standart output
	EXIT_SUCCESS:	equ 0			; exit code success
 	SYS_EXIT:		equ 60		; exit systemcall code
