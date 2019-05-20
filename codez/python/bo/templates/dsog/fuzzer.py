#!/usr/bin/env python

import sys
import socket
from time import sleep

# Invoke the script: ./fuzzer.py <target> <port>
t = sys.argv[1]
p = int(sys.argv[2])

# initial string -- 
b = '\x41' * 50

# loop --
while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	s.settimeout(2)
    	s.connect((t,p))

    	# send --
    	print "Sending buffer with length: " + str(len(b))
    	s.send(" " + b + "\n")
    	s.recv(1024)
    	s.close()
    	sleep(1)
    	# increase buffer --
    	b = b + '\x41'*50


    except:
        print "[+] Crash occured with buffer length: " + str(len(b) - 50)
        sys.exit()
