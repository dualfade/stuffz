#!/usr/bin/env python3
# template.py --
# @dualfade

# gen bad chars --
# pip install badchars
# badchars -f python | sed 's/^\s*\"./\tb"\\/g' \
# xclipc -selection clipboard

# skel refs --
# https://bit.ly/3KIIjzz --

import socket
import sys
from optparse import OptionParser

# from struct import pack

# defs --
# def eip_chain():
#     """ eip chain function -- """

#     gadgets = [
#         0xffffffff,         # ;
#         0xffffffff,         # ;
#         0xffffffff,         # ;
#     ]

#     # return eip --
#     return b''.join(pack('<L', _) for _ in gadgets)

# def rop_chain():
#     """ main rop chain function -- """

#     gadgets = [
#         0xffffffff,         # ;
#         0xffffffff,         # ;
#         0xffffffff,         # ;
#     ]

#     # return eip --
#     return b''.join(pack('<L', _) for _ in gadgets)

def payload_send():
    """ send payload function -- """

    # args --
    length = str(options.length)

    try:
        print('[info] sending payload')

        # initial \x41 test payload --
        buf = b"\x41" * int(length)
        sock_connect(buf)

    except OSError as err:
        error(err)
        sys.exit(-1)

def sock_connect(buffer):
    """ socket connect function --"""

    try:
        # args --
        port = int(options.port)
        target = str(options.target)

        print("[info]: sending => %s" % buffer)
        s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('%s' % target, port))
        s.send(buffer)

        # get resp --
        resp = s.recv(1024)
        print(resp)

        # finally close socket; ret resp --
        s.close()

    # except --
    except OSError as err:
        error(err)

def error(err):
    """ standard error message -- """

    print('[err] application error %s' % err)

# main --
if __name__ == "__main__":
    """ main function args -- """

    # parser opts --
    parser = OptionParser()
    parser.add_option('-t', '--target', dest='target', help='target ip address')
    parser.add_option('-p', '--port', dest='port', help='port')
    parser.add_option('-l', '--length', dest='legth', help='payload length')
    try:
        (options, args) = parser.parse_args()
        if (options.target):

            # start --
            print('[info] starting exploit')
            payload_send()
            sys.exit(-1)
        else:
            print('[err] missing input')
            print('[err] exiting')
            sys.exit(-1)
    except SystemExit:
        sys.stdout.write("\n")
        sys.stdout.flush()



#__eof__
