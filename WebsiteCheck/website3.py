#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Yuanzhi Bao'


import re

import urllib2

import argparse


def websiteToStr(parser, url, element=None, ele_keyword=None, Keyword=None):


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
    except:
        pass

    # urllib2 url wrong module, library.
    # handle redirect loop problem.

    if response:
        response_read = str(response.read())
    else:
        print("Something wrong with your input!!")
        print(parser.print_help())
        exit(2)

    if element and ele_keyword:

        element = element.lower()

        element_keyword = ele_keyword.lower()

        filtered_resp = re.findall(r"<%s>.*%s.*</%s>" % (element, element_keyword, element), response_read.lower())

        if not filtered_resp:
            print("There is no such element and keyword match!")

        return filtered_resp

    elif element:
        print ("With element, you must input the elekw (element keyword) following, for more information type --help")
    elif ele_keyword:
        print ("With ele_keyword, you must input the element before it, for more information type --help")

    if Keyword:

        filtered_resp = re.findall(r"%s" % Keyword, response_read.lower())

        if not filtered_resp:
            print("There is no such keyword match!")

        return filtered_resp

    return None


if __name__ == "__main__":


    parser = argparse.ArgumentParser("""
        This script is use to simply test whether a website contains certain keyword in it.
        element check must be used with elefw (element keyword).
        keyword can be used alone for testing whether a web page has the keyword.
        All input are not case sensitive.
    """)

    parser.add_argument('-url', '--url', type=str, action='store', help="input the url you want to test")

    parser.add_argument('-element', '--element', type=str, action='store', help="input the element you want to test, \
    must be used with elekw")

    parser.add_argument('-elekw', '--elekw', type=str, action='store', help="input the element keyword you want to test,\
     must be used with element")

    parser.add_argument('-keyword', '--keyword', type=str, action='store', help="input the keyword you want to test, \
    to use this, simply leave element and elekw alone, otherwise it won't do the job!")

    args = parser.parse_args()

    # Namespace(element=dwdw,keyword)
    # name the argument costume
    if args.element == None and args.elekw == None and args.keyword == None:
        print("There is no input!")
        exit(2)

    checkresult = websiteToStr(parser, args.url, args.element, args.elekw, args.keyword)


    if checkresult:
        # print("0")
        exit(0)
    else:
        print("2")
        exit(2)