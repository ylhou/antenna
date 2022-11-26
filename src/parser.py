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
    # import requests
    #
    # res = requests.get("https://s.weibo.com/realtime?q=电池&atten=1", cookies = set_cookies("SINAGLOBAL=663038985208.0864.1645453830742; SCF=AvB7kGmjoF832pPtYLTnggtdxrISaiD-jSh4QwSRo12_nvE2XSMO8MyIf8nvegfqVi4hiqKBAXRv33SZCC9n7iE.; _s_tentry=-; Apache=5513822977698.286.1669453453824; ULV=1669453453861:18:6:2:5513822977698.286.1669453453824:1669122051216; WBtopGlobal_register_version=2022112617; UOR=,,login.sina.com.cn; PC_TOKEN=779f6bbdca; SUB=_2A25OharlDeRhGeRO7lIR8yrKwjuIHXVt8pstrDV8PUNbmtANLUWmkW9NUHtg4y-RQKMiQ0jgNfkITXErSEzBvm04; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFxsjl64zmGGkzqUhTXpuwm5JpX5KzhUgL.Foz7SK57e0Bc1KM2dJLoIXnLxK.LB.BL1h2LxKBLB.-LB-qLxK-L1K5LB.eLxK-L12-L1-2LxKqL1-eL1h.LxKML1KBLBoMLxK-LB.eL1hzLxK-L1K2LB.et; ALF=1700990517; SSOLoginState=1669454517"))
    #
    # sys.exit()