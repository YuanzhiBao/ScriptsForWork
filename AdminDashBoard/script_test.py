#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'Yuanzhi Bao'


import psutil

import urllib



import requests

requests.get('https://api.github.com/user', auth=('user', 'pass'))


cpuData = psutil.cpu_times()

#处理数据

cpuMax = cpuData.user+cpuData.system+cpuData.idle

cpuUsed = cpuData.user+cpuData.system

cpuUse = cpuUsed/cpuMax


data = {"cpuUsed":cpuUse, "hostname": "windowsossom"}

#sendData = urllib.parse.urlencode(data)

#sendData = sendData.encode('utf-8')

url = "http://localhost:8000/dashboard/scripttest/"

header = {

        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",

    }

#定义请求

res =requests.post(url,data = data)

#req = urllib.request.Request(url,data = sendData,headers = header,method = 'POST')

#添加Header

#req.add_header(headers = header)

#发送请求

#ope = urllib.request.urlopen(req)

#打印结果

print(res.content.decode())

#print(ope.read())
