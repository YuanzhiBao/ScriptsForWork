#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'Yuanzhi Bao'

import json
import urllib2
data = json.dumps({ 'name':'apitest', 'pass':'this_is_temporary'})

url = "http://127.0.0.1:3000/auth"

req = urllib2.Request(url, data, {'Content-Type': 'application/json'})

f = urllib2.urlopen(req)

response = json.loads(f.read())

f.close()



print(type(response))

# print(response["token"])

url = "http://127.0.0.1:3000"


token = response["token"]

# token += "1"

req = urllib2.Request(url)

req.add_header('x-access-token', token)

f = urllib2.urlopen(req)

# wrong_token_response = json.loads(f.read())


data2 = json.dumps({"name":'testhost3', 'loadPct': 50})

print(data2)

url = "http://127.0.0.1:3000/host/add/"

req = urllib2.Request(url)

req.add_header('x-access-token', token)

req.add_header('content-type','application/json')

req.add_data(data2)

f = urllib2.urlopen(req)

print(f.read())




data2 = json.dumps({'name':'testhost'})

url = "http://127.0.0.1:3000/host/add/"

req = urllib2.Request(url)

req.add_header('x-access-token', token)

req.add_data(data2)

f = urllib2.urlopen(req)

# print(f.read())


url = "http://127.0.0.1:3000"


token = response["token"]

# token += "1"

req = urllib2.Request(url)

req.add_header('x-access-token', token)

f = urllib2.urlopen(req)

# print(f.read())


data2 = json.dumps({"name":'testhost3', 'loadPct': 100})

url = "http://127.0.0.1:3000/update/host/testhost3"

req = urllib2.Request(url)

req.add_header('x-access-token', token)
req.add_header('content-type','application/json')

req.add_data(data2)

f = urllib2.urlopen(req)

# print(f.read())


# print(type(wrong_token_response))


# if wrong_token_respons.contains_key["message"]
#     print("hi")
# print(wrong_token_response)

# print(wrong_token_response["message"])
# print(wrong_token_response["message"])
###ho dwo dwaodaw d



## next step: how to dealing with a invalid token? How to pass back an invalid token?

