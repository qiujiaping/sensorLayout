#!/usr/bin/env python
# encoding: utf-8
from main.GA.individual import individual
import wntr

'''
@author: 雨夜微凉
@contact: 1475477624@qq.com
@file: population.py
@time: 2020/5/13 11:28
@desc:产生种群
'''

class population:
    def __init__(self,pop_size:int,chrom_length:int,inp:str):
        """
        @param pop_size: 种群规模
        @param chrom_length: 染色体长度
        @param inp:
        """
        self.pop_size=pop_size
        self.populations=[]
        self.chrom_length=chrom_length
        self.inp=inp
        wn = wntr.network.WaterNetworkModel(self.inp)
        self.nodeIndexList = list(range(wn.num_junctions) )    #节点id范围

    def generatePopulations(self):
        for i in range(self.pop_size):
            self.populations.append(individual(self.chrom_length,self.nodeIndexList))

if __name__=="__main__":
    pops = population(100, 6, "D:/科研/code/sensorLayout/result/Net3.inp")
    pops.getPopulations()
    print(pops)