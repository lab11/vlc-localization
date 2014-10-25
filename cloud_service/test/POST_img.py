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
        headers={
            'content-type': 'image/jpeg',
            'X-luxapose-phone-type': 'lumia_1020',
            'X-luxapose-camera': 'back',
            'X-luxapose-ble-loc-hints': '4908',
            },
        data=open(fname, 'rb'))
        #files={fname:open(fname, 'rb')})
print(r.status_code)

