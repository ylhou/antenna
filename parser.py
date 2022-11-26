#!/urs/bin/env python
# -*- coding:utf-8 -*-
"""

:Author:  Houyanlong
:Create:  2022/11/24 22:27
Copyright (c) 2018, Lianjia Group All Rights Reserved.
"""
import json
import time
from datetime import datetime


class Parser(object):
    def __init__(self, id):
        self.id = id

    def execute(self, text):
        if self.id == 'P101':
            resp = json.loads(text)
            if resp.get("app_msg_list"):
                t = resp["app_msg_list"][0]["create_time"]
                if datetime.fromtimestamp(time.time()).day == datetime.fromtimestamp(t).day:
                    return {"msg": "猫笔刀", "id": self.id}


if __name__ == '__main__':
    pass
