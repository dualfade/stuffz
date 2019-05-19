#!/usr/bin/env python
import socket

# target --
RHOST = "192.168.0.139"
RPORT = 31337

# create socket --
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RHOST, RPORT))

# test message --
buf = ""
buf += "automated script"
buf += "\n"

# send the buffer --
s.send(buf)

# print sent --
print "Sent: {0}".format(buf)

# recieve data --
data = s.recv(1024)

# print recv --
print "Recv: {0}".format(data)
