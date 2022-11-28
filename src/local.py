#!/urs/bin/env python
# -*- coding:utf-8 -*-
"""

:Author:  Houyanlong
:Create:  2022/11/27 22:42
Copyright (c) 2018, Lianjia Group All Rights Reserved.
"""

import requests
import json
from pandas import DataFrame
import time

COUNTING = 5
SLEEP = 60
def set_cookies(cookie_str):
    cookie_dict = {}
    if len(cookie_str) > 0:
        cookie_arr = cookie_str.split(';')
        for c in cookie_arr:
            k, v = c.strip().split('=', 1)
            cookie_dict[k] = v
    return cookie_dict
class LocalProcess(object):
    def __init__(self, url):
        self.url = url
        self.cookies = 'tvfe_boss_uuid=059120f738f7d3c7; pgv_pvid=9881235328; pac_uid=0_099f7c91990a1; iip=0; ua_id=YkEbfy4fj7FOKAi3AAAAAAWEqkEKp_5awjXtBqkPi4k=; mm_lang=zh_CN; rand_info=CAESIKE6qdFFKjFALQ1WbgyilZyeplwuTFcphZWRYKciWaNC; slave_bizuin=3078275801; data_bizuin=3078275801; bizuin=3078275801; data_ticket=TCCxq8M5NRSJMCJp2io8X5i9/JJM8KAID3sDp9QVtLPab9zzw/GVqReL34vViW2S; slave_sid=dVZhNThxeUpDVTdpM0ozaEVkYmozYlVwb0M3cHVYd28yN2lZM192Q2FONzU5SndFS0lEUmpNeXcxdVFCTzZhdUNxZU5NTEpUMmtEdG9lS0xhNFZBQzExYWZKaWN2V0tkNGVTWENYT2x4dkQ4VUpFcHczR29ieG55ZllEcU43QlJnMU9QNU5EcnVuNFF6ZDB1; slave_user=gh_18ffd488972d; xid=032ffc4459d663010daaa5eb82c49e6e; _clck=3078275801|1|f6v|0'

    def parse(self):
        comment_dict = {}
        count_down = COUNTING
        while 1:
            l = len(comment_dict.keys())
            res = requests.get(self.url, cookies=set_cookies(self.cookies))
            comments = json.loads(res.text)["elected_comment"]
            for item in comments:
                id = item["id"]
                content = item["content"]
                reply=""
                if item["reply_new"].get("reply_list") and len(item["reply_new"]["reply_list"]) > 0:
                    reply = item["reply_new"]["reply_list"][0]["content"]
                if comment_dict.get(id):
                    if len(comment_dict[id]["reply"]) == 0 and len(reply) > 0:
                        comment_dict[id]["reply"] = reply
                else:
                    comment_dict[id] = {"content":content,"reply":reply}

            if len(comment_dict.keys()) == l:
                count_down -= 1
            else:
                count_down = COUNTING
            if count_down == 0:
                break
            time.sleep(SLEEP)
        return comment_dict


if __name__ == '__main__':
    url = "https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&scene=0&appmsgid=2247499316&idx=1&comment_id=2685210642511577089&offset=0&limit=100&send_time=&sessionid=svr_52239f6658f&enterid=1669645476&uin=NTkxMDkzNzM1&key=97cf597273159342851f3c9cee1c5e266d06b5b012560b001ee55fc4dedf310a400bd88c1e3aea07e78df94f10768f3068b6e635ac9406c7d49f1e134079bc28ab3ca647c41a616910f48ca9bc68689eb231f8a10e27345fa084fa737cefad43cc8833f751d400e8b860edb514bde784bde56c14e45897a02a9ae88fe69a9c05&pass_ticket=gul9%2B5XgxeCqcSgvOWki2Z%2FkeGWamPE2j4oInwh%2Br2EZtLh%2FMy7cu%2FkJuFwFKc6b&wxtoken=777&devicetype=iMac%26nbsp%3BMacBookPro16%2C1%26nbsp%3BOSX%26nbsp%3BOSX%26nbsp%3B12.5.1%26nbsp%3Bbuild(21G83)&clientversion=13060110&__biz=Mzg2NzcxMjE1NA%3D%3D&appmsg_token=1193_AZovZqNwBhOVf9cc5Q8Q7UL89l0PhpF4ilk82fh5gHyefX50l_anMMWzNAxz8mIjemn-v5NzE4XQekk6&x5=0&f=json"
    print(LocalProcess(url).parse())
