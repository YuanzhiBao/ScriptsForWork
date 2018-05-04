#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'Yuanzhi Bao'


def fib(n):

    a,b = 0,1

    while a < n:
        a, b = b, a+b
        print(a,b)


# fib(1000)

def fib2():
    pass

# print(None)

# print(fib2())

import time

def f2(a, stamp = time.strftime('%Y-%m-%d %H:%M:%S')):
    time.sleep(1)
    stamp2 = time.strftime('%Y-%m-%d %H:%M:%S')
    stamp = time.strftime('%Y-%m-%d %H:%M:%S')
    print(a, stamp)
    print(a, stamp2)


def f(a, L=None):
    if L is None:
        L = []
    L.append(a)
    return L







pairs = [(1, 'one'), (6, 'two'), (3, 'three'), (4, 'four')]


a = ['dwad','fwaf','dwadwa']

c = list(map(list,a))

print(c)

d= list(map(lambda x:x[1]+"x",c))


a = [1,2,3,4]
b = ['a','b','c','d']

e = [(x,y) for x in a for y in b]

f = (zip(a,b))

x = map(lambda x,y:(x,y), a,b)

print(list(x))

a = set("dwdawfawf")



print(a)

print(f)






# b = list(map(lambda x:x+"x",list(map(list, a))))

# print(b)





# import indentation





if __name__=="__main__":
    print("nilegequhuiwan")

import sound.effects.echo as hehe

hehe.houhou()


x = 10 * 3.25
y = 200 * 200


print(repr((x, y, ('spam', 'eggs'))))

print(str((x, y, ('spam', 'eggs'))))


for x in range(1, 11):
    print(repr(x).rjust(5), repr(x*x).rjust(3))
# Note use of 'end' on previous line
    print(repr(x*x*x).rjust(4))

with open("test.txt",'w') as f:
    read_date = f.write("dwdwdwdwdw")

with open("test.txt","r") as f:
    read_date = f.read()

f = open("test.txt",'r+')



# print(read_date)

import json

print(type(json.dumps([1,2,3,4])))

json.dump([1,2,3,4],f)

f = open("test.txt", 'r+')

x = json.load(f)

print(x)


import sys

try:
    f = open('myfile.txt')
    s = f.readline()
    i = int(s.strip())
except OSError as err:

    s = err.__str__()
    print(type(s))
    print(err.__str__())
except ValueError:
    print("Could not convert data to an integer.")
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise


a  = [1,2,3,4,5]

for i,j in enumerate(a):
    print(i, j)


