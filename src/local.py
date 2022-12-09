#!/urs/bin/env python
# -*- coding:utf-8 -*-
"""

:Author:  Houyanlong
:Create:  2022/11/27 22:42
Copyright (c) 2018, Lianjia Group All Rights Reserved.
"""

import requests
import json
import time
import argparse

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
    def __init__(self, url, cookies):
        self.url = url
        self.cookies = cookies

    def parse(self):
        comment_dict = {}
        count_down = COUNTING
        while 1:
            l = len(comment_dict.keys())
            res = requests.get(self.url, cookies=set_cookies(self.cookies))
            text = json.loads(res.text)
            if text.get('errmsg') and text['errmsg'] == "no session":
                break
            comments = text["elected_comment"]
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
    # url = "https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&scene=0&appmsgid=2247499374&idx=1&comment_id=2698253869460242433&offset=0&limit=100&send_time=&sessionid=svr_973154d4be7&enterid=1670420976&uin=NTkxMDkzNzM1&key=62364c8b1d0429a3a78cf401e76a8ca416d9e2ddfce12eaf2fde69dbe41823d6366ba1d6e0083191a111bc5ea32a92ea47804ae77d2ef6a52adee3300dd507db5ba6e10215e48029164c2d69ede28aeb6b2ff75bb1baad0db4fbecb1fd704590f362cd79e7ed88b1ad2529cc6a9e060b4798b16afb6d260d6e809f2cd9fd6f7a&pass_ticket=NI1%2Fnms2AMnx7dr4T%2BnWLvtZt1ij6wy2VKa4RokIag08K0jooq4voi2xq7xuv9uG&wxtoken=777&devicetype=iMac%26nbsp%3BMacBookPro16%2C1%26nbsp%3BOSX%26nbsp%3BOSX%26nbsp%3B12.5.1%26nbsp%3Bbuild(21G83)&clientversion=13060110&__biz=Mzg2NzcxMjE1NA%3D%3D&appmsg_token=1195_2bWzmvYFFOr8HXcxwGoaIpVeN3FPF6aZNT8lpjRVsTixaNCnSbTUgVsleETkyxsCz9jgoE_k2DQ2hJoU&x5=0&f=json"
    cookies = 'appmsg_token=1194_28c4igjp2W78Sg9LiGYnv6VWpgFqxdULGtGkC63Ef4QJ5l7aHL9D4zSdpM8LfKIE6qMtWs9FsMv12dyu; devicetype=iMacMacBookPro161OSXOSX12.5.1build(21G83); lang=zh_CN; pass_ticket=Ad3/q+7sLGVwzY91V9ssnsuZ+6UbBWkU8+yNc10Mh9h1SMrgApi3m2EO6VOhE49U; rewardsn=; version=13060110; wap_sid2=COe/7ZkCEooBeV9IRUZHYlZycVJFQTN3ZjJnUks4SG1XeVZnYUJ3ak5CMXN5eTc0ZktobUpLaGgwb3ZrTHh5cGI1cXRwUjZZMWFCZ0tKcldjQmx3bUR6SDhyYjVoQl9XTGJNRTJ5NmZVOE1SZ1duM1FTLVhqZHRnREVBQnhOdTVHelVPNWs4ck1KWGRvZ1NBQUF+MO/zt5wGOA1AAQ==; wxtokenkey=777; wxuin=591093735; wwapp.cst=; wwapp.deviceid=; wwapp.vid='
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', required=False, type=str)
    args = parser.parse_args()

    print(LocalProcess(args.url, cookies).parse())
