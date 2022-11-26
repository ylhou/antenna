#!/urs/bin/env python
# -*- coding:utf-8 -*-
"""

:Author:  Houyanlong
:Create:  2022/11/16 16:29
Copyright (c) 2018, Lianjia Group All Rights Reserved.
"""
import http.client, urllib

class Msger:
    def __init__(self, token, key):
        self.token = token
        self.key = key

    def send(self, msg):
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
                     urllib.parse.urlencode({
                         "token": self.token,
                         "user": self.key,
                         "message": msg,
                     }), {"Content-type": "application/x-www-form-urlencoded"})
        conn.getresponse()


if __name__ == '__main__':
    pass
