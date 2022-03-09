# Generic shellcode payload exploit makefile
# Note: For buffer overflow, disable ASLR using `sudo sysctl -w kernel.randomize_va_space=0`

# Variables:
# 1. shellcode binary
SHELLCODE=./hello_world
# 2. victim stack binary
VICTIM_BIN=./victim-exec-stack
# 3. victim function of binary
VICTIM_FUN=main
# 4. file to store payload
PAYLOAD_FILE=./bo_payload.txt
# 5. payload generator file
PAYLOAD_GENERATOR=./bo_generator.py

# Used to compile shellcode
compile_shellcode:
	nasm -f elf64 $(SHELLCODE).asm -o $(SHELLCODE).o
	ld -m elf_x86_64 $(SHELLCODE).o -o $(SHELLCODE)
# Used to test shellcode binary: This running does not necessary mean the binary can be used as shellcode. `make exploit` can be used to check working of shellcode.
run_shellcode:
	$(SHELLCODE)
# Used to test shellcode or to exploit the given binary
exploit:
	$(PAYLOAD_GENERATOR) $(VICTIM_BIN) $(VICTIM_FUN) $(SHELLCODE) $(PAYLOAD_FILE)
	$(VICTIM_BIN) < $(PAYLOAD_FILE)
# Remove generated files
clean:
	rm -f $(SHELLCODE).o $(SHELLCODE) $(PAYLOAD_FILE)
