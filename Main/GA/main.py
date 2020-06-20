#!/usr/bin/env python
# encoding: utf-8
from population import population
import numpy as np
from simulation.readAndDraw import loadSensitiveMat
import wntr
import matplotlib.pyplot as plt
import time
import random
from Main.tools import disAndNodeDir
from copy import copy
from Main.GA.cross import cross
from Main.GA.selection import selection
from Main.GA.mutation import mutation
from Main.GA.calFiteness import calFiteness
from Main.GA.population import population
'''
@author: 雨夜微凉
@contact: 1475477624@qq.com
@file: main.py
@time: 2020/5/9 17:41
@desc:  这是布局算法的入口
'''

class ga:
    def __init__(self,pop_size:str,chrom_length:str,pc:str,pm:str,iteration:int,inp=None):
        """
        @param pop_size: 种群规模
        @param chrom_length: 染色体长度
        @param pc: 交叉概率
        @param pm: 变异概率
        @param iteration: 迭代次数
        """
        self.pop_size =pop_size
        self.chrom_length=chrom_length
        self.pc=pc
        self.pm=pm
        self.iteration=iteration
        self.eachGeneBestValue=[] #存放每一代最好值[[适应度，个体]]
        self.inp=inp
        wn=wntr.network.WaterNetworkModel(inp)
        nodeID=wn.junction_name_list
        self.nodeIdIndex={}
        for i in range(len(nodeID)):
            self.nodeIdIndex.update({nodeID[i]:i})
        self.nodeIndexList = list(range(len(nodeID)))  # 节点id范围
        self.disMat=disAndNodeDir.distance(self.inp)

    """
        ga算法的启动函数
    """
    def run(self,senMat):
        """
        @param senMat: 敏感度矩阵
        """
        senMat=senMat.T #转置使得行为节点，列为泄漏点
        Pops=population(self.pop_size,self.chrom_length,self.inp)
        fitness= calFiteness(Pops,self.disMat,senMat)
        for  i in range(self.iteration):
            start=time.clock()
            # 复制一份父代
            parents=Pops.copy()
            # 记录该代最好的
            values=list(fitness.values())
            keys=list(fitness.keys())
            print(values[0])
            self.eachGeneBestValue.append([values[0],Pops[keys[0]]]) #存放每一代最好的值
            #产生子代
            childs=selection(Pops,fitness)   #选择
            cross(childs,self.pop_size,self.pc,self.chrom_length)               #交叉
            mutation(childs,self.pop_size,self.chrom_length,self.pm,self.nodeIndexList)            #变异
            # 子代和父代混合，选取前一半最好适应度的个体（精英保留策略）
            parents_childs= np.vstack((parents, childs))
            fitness={}
            Pops = []
            index=0
            for key,value in list(calFiteness(parents_childs,self.disMat,senMat).items())[:self.pop_size]:
                fitness.update({index:value})
                Pops.append(parents_childs[key])
                index=index+1
            end = time.clock()
            print("第%s代"%i,"耗时：",end-start,"秒")


        self.resultPlot()

    def resultPlot(self):
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        x = []
        y = []
        for i in range(self.iteration):
            x.append(i)
            y.append(self.eachGeneBestValue[i][0])
        plt.plot(x, y)
        plt.xlabel('代数')
        plt.ylabel("value")
        plt.show()

    # def best(self,fitness,Pops):
    #         """
    #         @param fitness: 适应度
    #         @param Pops: 种群
    #         @return: 最好个体所对应的适应度，个体（染色体为节点的索引从0开始）
    #         """
    #         best_value=np.min(fitness)
    #         index=np.where(fitness== best_value)    #index为元组类型这里提取第一个元素
    #         best_individual=copy(Pops.populations[index[0][0]].chromosome)
    #         return best_value,best_individual


if __name__=="__main__":                                                                                                                                                             
    g=ga(100,50,0.6,0.2,120,"D:/科研/code/sensorLayout/result/CTOWN.INP")
    unitMat=loadSensitiveMat("D:/科研/code/sensorLayout/result/CTOWN.csv")
    g.run(unitMat)


















