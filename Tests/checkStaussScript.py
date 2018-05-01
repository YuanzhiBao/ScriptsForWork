#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Yuanzhi Bao'


import re

import urllib2

import argparse


def websiteToStr(parser, url, element=None, keyword=None):


    if url.startswith(("http://","https://")):
        httpurl = url
    else:
        httpurl = "https://" + url


    try:
        response = urllib2.urlopen(httpurl)
    except urllib2.HTTPError as a:
        print(a)
        print("****404 NOt FOUND --> The page you are testing is not found****")
        if not httpurl.endswith("/"):
            print("Maybe you forgot \"/\" at the end of the url??")
        print(parser.print_help())
        exit(2)
    except urllib2.URLError as b:
        print(b)
        print("****BAD URL --> The page you are testing is invalid****")
        exit(2)
    except urllib2.HTTPErrorProcessor as p:
        print(p)
        exit(2)
    except Exception as e:
        print(e)
        exit(2)

    # urllib2 url wrong module, library.
    # handle redirect loop problem.

    if response:
        response_read = str(response.read())
    else:
        print("Something wrong with your input!!")
        print(parser.print_help())
        exit(2)

    # lower the case
    if element:
        element = element.lower()

    if keyword:
        keyword = keyword.lower()


    if element and keyword:

        filtered_resp = re.findall(r"<%s>.*%s.*</%s>" % (element, keyword, element), response_read.lower())

        if not filtered_resp:
            print("There is no such element and keyword match!")

        return filtered_resp

    elif element:
        print ("With element, you must input keyword following, for more information type --help")
    elif keyword:
        filtered_resp = re.findall(r"%s" % keyword, response_read.lower())

        if not filtered_resp:
            print("There is no such keyword match!")

        return filtered_resp

    return None


if __name__ == "__main__":


    parser = argparse.ArgumentParser("""
        This script is use to simply test whether a website contains certain keyword in it.
        element check must be used with keyword.
        keyword can be used alone for testing whether a web page has the keyword.
        All input are not case sensitive.
    """)

    parser.add_argument('-url', '--url', type=str, action='store', help="input the url you want to test")

    parser.add_argument('-element', '--element', type=str, action='store', help="input the element you want to test, \
    must be used with keyword")

    parser.add_argument('-keyword', '--keyword', type=str, action='store', help="input the keyword you want to test, \
    will search for just the keyword if you leave element alone.")

    args = parser.parse_args()

    # Namespace(element=dwdw,keyword)
    # name the argument costume
    if args.element == None and args.keyword == None:
        print("There is no input!")
        exit(2)

    checkresult = websiteToStr(parser, args.url, args.element, args.keyword)


    if checkresult:
        # print("0")
        exit(0)
    else:
        # print("2")
        exit(2)