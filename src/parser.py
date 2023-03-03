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
                    print("今天的文章已发")
                    return {"msg": "猫笔刀", "id": self.id}
            elif resp.get("base_resp"):
                if resp["base_resp"].get("err_msg"):
                    return {"msg": "猫笔刀%s" % (resp["base_resp"]["err_msg"]), "id": self.id}
            else:
                return {"msg": "猫笔刀(bad resp)", "id": self.id}
        if self.id == 'P201':
            pass
        if self.id == 'P301':
            resp = json.loads(text)
            if resp["message"] == 'OK':
                data = resp["data"]
                msg = []
                titles = []
                if data.get('items') and len(data['items']) > 0:
                    for item in data['items']:
                        if int(item["display_time"]) > int(time.time()-60*60*24):
                            title = item["title"]
                            if title in titles:
                                continue
                            if  title.strip() == '':
                                continue
                            titles.append(title)
                            msg.append(item["content_text"])
                return {"msg": "/".join(msg), "id": self.id}
            else:
                return {"msg": "华尔街(bad resp)", "id": self.id}





if __name__ == '__main__':
    pass