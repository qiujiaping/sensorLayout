#!/usr/bin/env python
# encoding: utf-8
'''
@author: 雨夜微凉
@contact: 1475477624@qq.com
@file: test.py
@time: 2020/5/13 22:02
@desc:
'''

class Dog:
    def __init__(self,age):
        self.age=age


if __name__=="__main__":
    a=[Dog(i) for i in range(3) ]

    prent=a[:]
    for i in a:
        i.age=8
    child=a.copy()

    d = {'lilee': 25, 'wangyan': 21, 'liqun': 32, 'age': 19}
    a={}





