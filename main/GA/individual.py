#!/usr/bin/env python
# encoding: utf-8
import random

'''
@author: 雨夜微凉
@contact: 1475477624@qq.com
@file: individual.py
@time: 2020/5/13 11:29
@desc:产生个体
'''

class individual:
    def __init__(self,chrom_length,nodeIndexList):

        """
        @param chrom_length: 染色体长度
        @param nodeIndexList: 节点索引列表（从0开始算起）

        每个个体包含适应度

        """
        self.chrom_length=chrom_length
        self._chromosome=sorted(random.sample(nodeIndexList,chrom_length))
        self.fitness = None     #可以选择是否包含适应度

    @property
    def chromosome(self):
        return self._chromosome

    @chromosome.setter
    def chromosome(self,value):
        self._chromosome=value




if __name__=="__main__":
    a=individual(6,range(20))
    print(a)

