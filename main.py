#!/urs/bin/env python
# -*- coding:utf-8 -*-
"""

:Author:  Houyanlong
:Create:  2022/11/15 22:58
Copyright (c) 2018, Lianjia Group All Rights Reserved.
"""
import os
import yaml
import sys
import argparse
import time
from math import floor
from datetime import datetime
import asyncio
import aiohttp
from collections import OrderedDict
from src.parser import Parser
from src.messager import Msger


def stamp_to_struct(seconds):
    t = datetime.fromtimestamp(seconds)
    return {
        "DAYOFMONTH": t.day,
        "WEEKDAY": t.weekday(),
        "MONTHOFYEAR": t.month,
        "DATE": t.strftime("%Y-%m-%d")
    }

def date_to_stamp(hm):
    d = "%s %s" % (T["DATE"], hm)
    return floor(datetime.strptime(d, "%Y-%m-%d %H:%M").timestamp())


def load_config(path):
    with open(path, 'r', encoding='utf-8') as file:
        uc = yaml.safe_load(file)
    return uc


def set_cookies(cookie_str):
    cookie_dict = {}
    if len(cookie_str) > 0:
        cookie_arr = cookie_str.split(';')
        for c in cookie_arr:
            k, v = c.strip().split('=', 1)
            cookie_dict[k] = v
    return cookie_dict


def set_timeline(cfg):
    line = []
    todo = {}

    def schedule(timepoint, event):
        for t in timepoint:
            if t not in line:
                line.append(t)
            if t not in todo:
                todo[t] = [event]
            else:
                todo[t].append(event)

    if cfg.get("matters"):
        matters = cfg["matters"]
        for item in matters:
            if item.get("repeat_at"):
                if T[item["category"]] not in item["repeat_at"]:
                    continue
            tl = [date_to_stamp(tp) for tp in item["start_at"]]
            schedule(tl, {
                "msg": item["msg"]
            })

    if cfg.get("sniffers"):
        for page in cfg["sniffers"]:
            # cookies = set_cookies(page["cookies"])
            cookies = page["cookies"]
            if page.get("start_at"):
                # 一级页面
                pass
            else:
                # 二级页面
                for item in page["subpage"]:
                    if item.get("repeat_at"):
                        if T[item["category"]] not in item["repeat_at"]:
                            continue
                    if item.get("end_at"):
                        tp = date_to_stamp(item["start_at"])
                        end = date_to_stamp(item["end_at"])
                        tl = []
                        while tp <= end:
                            tl.append(tp)
                            tp += item["clock_freq"]
                    else:
                        tl = [date_to_stamp(tp) for tp in item["start_at"]]

                    schedule(tl, {
                        "url": page["base_url"] % tuple(item["queries"]),
                        "cookies": cookies,
                        "id": item["parser_id"],
                        "repeat": item["repeat"]
                    })

    return sorted(line), OrderedDict(sorted(todo.items()))


async def fetch(url, cookies):
    async with aiohttp.ClientSession(headers={
        "cookie": cookies
    }) as session:
        async with session.get(url) as res:
            text = await res.text()
            return text


async def parse(text, id):
    p = Parser(id)
    resp = p.execute(text)
    del p
    return resp


async def crawl(evt):
    r = await fetch(evt["url"], evt["cookies"])
    result = await parse(r, evt["id"])
    return result


async def clock(intervals):
    print("tick")
    await asyncio.sleep(intervals)


async def workflow(intervals, event_list):
    coroutine_list = [clock(intervals)]
    for evt in event_list:
        coroutine_list.append(crawl(evt))
    tasks = [asyncio.ensure_future(coroutine) for coroutine in coroutine_list]
    dones, pendings = await asyncio.wait(tasks)
    msg_list = []
    for f in dones:
        print(f._coro, f.result())
        if f.result():
            msg_list.append(f.result())
    return msg_list

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', required=True, type=int, help='运行模式（1.shell/2.docker）')
    parser.add_argument('-u', '--url', required=False, type=str, help='shell模式下本地爬虫链接')
    args = parser.parse_args()
    global T
    T = stamp_to_struct(time.time())
    filepath = "user_config.yml"
    if args.mode == 2:
        filepath = "/cfg/user_config.yml"
    user_config = load_config(filepath)
    time_line, todolist = set_timeline(user_config)
    messager = Msger(user_config["pushover"]["api_token"], user_config["pushover"]["usr_key"])
    just_now = time_line[0]
    while len(time_line) > 0:
        # 是否更新了配置文件
        cfg_msec = floor(os.path.getmtime(filepath))
        cfg_mtime = stamp_to_struct(cfg_msec)
        if cfg_mtime["DATE"] == T["DATE"] and cfg_msec > just_now:
            user_config = load_config(filepath)
            time_line, todolist = set_timeline(user_config)
            just_now = cfg_msec
            continue
        now = floor(time.time())
        coming = time_line[0]
        if now > coming:
            time_line.pop(0)
            continue
        if len(todolist[coming]) == 0:
            time_line.pop(0)
            continue
        interval = time_line[0] - now
        time_line.pop(0)
        # 做一轮任务
        coro_list = []
        notice_list = []
        messages = []
        for evt in todolist[coming]:
            if evt.get("url"):
                coro_list.append(evt)
            else:
                notice_list.append(evt)
        coro_results = asyncio.run(workflow(interval, coro_list))
        for c in coro_results:
            if len(c["msg"]) > 0:
                messages.append(c["msg"])
            for tp in list(time_line):
                for evt in list(todolist[tp]):
                    if evt.get("id"):
                        if evt["repeat"] == "ONCE":
                                if evt["id"] == c["id"]:
                                    todolist[tp].remove(evt)
                if len(todolist[tp]) == 0:
                    del todolist[tp]
                    time_line.remove(tp)

        for n in notice_list:
            messages.append(n["msg"])
        if len(messages) > 0:
            messager.send("「" + "」「".join(messages) + "」")
        just_now = now

    sys.exit()