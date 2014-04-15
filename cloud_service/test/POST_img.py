#!/usr/bin/env python

import requests
import sys
import os

if len(sys.argv) < 2:
    print('One arg (file) req\'d')
    sys.exit(1)

fname = sys.argv[1]

try:
    host = sys.argv[2]
except IndexError:
    host = 'localhost'

r = requests.post('http://'+host+':4908/img/'+os.path.basename(fname),
        headers={'content-type': 'image/jpeg'},
        data=open(fname, 'rb'))
        #files={fname:open(fname, 'rb')})
print(r.status_code)

