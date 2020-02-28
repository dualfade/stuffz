#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# scriptname.py
# user[at]domain.com

# import --
import os
import sys
import urllib
import requests

# globals --


# definitions --
def Start_Function():
    print("something")


# main --
if __name__ == '__main__':
    try:
        argname1 = sys.argv[1]
        argname2 = sys.argv[2]
        argname3 = sys.argv[3]
    except IndexError:
        print("[-] Usage: %s target lhost lport" % sys.argv[0])
        sys.exit()

# start sploit --
Start_Function(argname1, argname2, argname2)

# __EOF__
