#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'Yuanzhi Bao'

lis = [1,2,3,4,5]

lis.insert(3,"dwa")

# lis.clear()

lis.count(2)

lis2 = lis[:]

lis.clear()

print(lis2)

print(lis.insert(0,1))

# print(lis.index(1))

# print(lis.count(4))

print(lis)

from collections import *

squares = []
for x in range(10):
    squares.append(x**2)

print(squares)

print(x)

squares = list(map(lambda x: x**2, range(10)))


a = deque(lis2)

print(a)


fwfw = 'nishiyizhizhu'

from Tests import test1

print(dir(test1))
