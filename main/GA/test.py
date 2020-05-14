#!/usr/bin/env python
# encoding: utf-8
'''
@author: 雨夜微凉
@contact: 1475477624@qq.com
@file: test.py
@time: 2020/5/13 22:02
@desc:
'''
from abc import ABCMeta, abstractmethod
class animal(metaclass=ABCMeta):
    def __init__(self):
        self.value=5

    @abstractmethod
    def say(self):
        """"""



class dog(animal):
    def __init__(self):
       pass

    def say(self):
        print("ssssss")


if __name__=="__main__":
    d=dog()
    d.say()

