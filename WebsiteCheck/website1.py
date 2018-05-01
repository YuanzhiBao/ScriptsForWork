#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Yuanzhi Bao'

# Usage: ./website2.py "url=www.google.com, title=googled"

import re
from sys import argv

import urllib2


print("dwa")
def toDict(s):
    result = {}
    for piece in s.split(","):
        key,value = piece.split("=")
        result[key.strip()] = value.strip()
    return result


def websiteToStr(url, dict):
    httpurl = "https://"+ url

    response = urllib2.urlopen(httpurl)

    response_read = str(response.read())


    keyword = dict.keys()[1].lower()

    value = dict.values()[1].lower()

    filtered_resp = re.findall(r"<%s>.*%s.*</%s>" %(keyword, value, keyword) ,response_read.lower())

    return filtered_resp


if __name__ == "__main__":

    try:
        dict = toDict(argv[1])
        checkresult = websiteToStr(dict["url"], dict)
    except:
        print "Usage example: ./website2.py \"url=www.google.com, title=google\""
        exit(2)

    if checkresult:
        exit(0)
    else:
        exit(2)
