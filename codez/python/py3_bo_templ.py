#!/usr/bin/env python3
# py3_bo_templ.py --
# dualfade

import sys
import socket
from optparse import OptionParser

# globals --

# defs --
def send():
    """ send payload -- """

    # args --
    port = int(options.port)
    target = str(options.target)
    buffer = str(options.buffer)

    try:
        print('[+] sending payload')

        # send junk --
        buffer = b"A" * int(buffer)

        """ send payload -- """
        s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('%s' % target, port))
        print("[info]: sending => %s" % buffer)
        s.send(buffer)
        resp = s.recv(1024)
        print(resp)

        # close --
        s.close()

        print('[+] done')

    except socket.error as e:
        print('[!] socket error: %s' % e)
        sys.exit(-1)


# main --
if __name__ == "__main__":
    """ get parser opts -- """
    parser = OptionParser()
    parser.add_option('-t', '--target', dest='target', help='target ip address')
    parser.add_option('-p', '--port', dest='port', help='port')
    parser.add_option('-b', '--buffer', dest='buffer', help='buffer length')
    try:
        (options, args) = parser.parse_args()
        if (options.target):
            """ send payload to target -- """
            print('[+] starting exploit')
            send()
            sys.exit(-1)
        else:
            print('[!] missing input')
            print('[!] exiting')
            sys.exit(-1)
    except SystemExit:
        sys.stdout.write("\n")
        sys.stdout.flush()
