#!/usr/bin/env python
# encoding: utf-8
'''
@author: 雨夜微凉
@contact: 1475477624@qq.com
@file: test.py
@time: 2020/5/13 22:02
@desc:
'''

class animal:
    def __init__(self):
        self.value=5

class dog:
    def __init__(self):
        self.collection=[animal() for i in range(2)]
if __name__=="__main__":
    d=dog()
    a=d.collection
    print(a[0].value)
    value=a[0].value
    value="assdssa"
    print(value)

