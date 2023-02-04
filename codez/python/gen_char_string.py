#!/usr/bin/env python3
# gen_char_string.py

#NOTE: ex --
# [0] % python gen_char_string.py -s 'id'
# 04-Feb-23 12:15:11 - [+] string val => id
# 04-Feb-23 12:15:11 - [+] chr conversion => chr(105).chr(100)

import sys
import logging
from optparse import OptionParser

# logging options --
logger = logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)

def do_charcode(s):
    """ generate charcode string from test -- """

    logging.info('[+] string val => %s' % s)
    new = []
    for i, l in enumerate(s):
        c = ord(l)
        new.append('chr(%s)' % c)

    return new

def error(err):
    """ standard error message -- """

    logging.error('[err] application error %s' % err)
    logging.error('[err] exiting now.')
    sys.exit(-1)

if __name__ == "__main__":
    """ main function args -- """

        # parser opts --
    parser = OptionParser()
    parser.add_option('-s', '--string', dest='string', help='str to convert')

    try:
        (options, args) = parser.parse_args()
        if (options.string):
            val = do_charcode(options.string)
            f = '.'.join(val)
            logging.info('[+] chr conversion => %s' %f )
        else:
            error('[!] missing input')

    # log; exit --
    except SystemExit as err:
        sys.stdout.write("\n")
        sys.stdout.flush()
