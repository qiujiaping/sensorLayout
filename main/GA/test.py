#!/usr/bin/env python
# encoding: utf-8
'''
@author: 雨夜微凉
@contact: 1475477624@qq.com
@file: test.py
@time: 2020/5/13 22:02
@desc:
'''
import matplotlib.pyplot as plt
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
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 在坐标轴上显示节点重要性图
    plt.plot(list(range(10)), [fiteness for fiteness in range(10)],
             marker="o", label="节点号-重要性图")
    # plt.xticks(range(self.iteration), range(self.iteration), rotation=90)
    plt.xlabel('代数')
    plt.ylabel("平均互相干系数")
    plt.show()





