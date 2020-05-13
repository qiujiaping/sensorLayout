#!/usr/bin/env python
# encoding: utf-8
from main.GA.population import population
import numpy as np
from simulation.readAndDraw import loadSensitiveMat
import wntr
import matplotlib.pyplot as plt
import time

'''
@author: 雨夜微凉
@contact: 1475477624@qq.com
@file: start.py
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

    """
        ga算法的启动函数
    """
    def startCalculate(self,senMat):
        """
        @param senMat: 敏感度矩阵
        """
        senMat=senMat.T #转置使得行为节点，列为泄漏点
        Pops=population(self.pop_size,self.chrom_length,self.inp)
        Pops.generatePopulations()   #产生初始种群
        for  i in range(self.iteration):
            start = time.clock()
            fitness=self.calFiteness(Pops,senMat)
            fitnessTime = time.clock()
            best_value,best_individual=self.best(fitness,Pops)
            print('适应度计算耗时%s' % (fitnessTime - start), '第%s代最好适应度:'%i,best_value)
            self.eachGeneBestValue.append([best_value,best_individual]) #存放每一代最好的值
            self.selection(Pops,fitness)   #选择
            self.cross(Pops)               #交叉
            self.mutation(Pops)            #变异
            eachGeneTime=time.clock()
            print('第',i,'代计算耗时%s' % (eachGeneTime - start))


    """
    计算适应度
    """
    def calFiteness(self,Pops,senMat:np.ndarray)->np.ndarray:
        """
        @param initPops: 种群
        @param senMat: 敏感度矩阵senMat.shape=[n，leaks]
        @return: 适应度(每个个体的平均互相干系数)
        """
        individualList=Pops.populations #引用类型，会把种群里的实例数据更改
        fitness=[]
        n,leaks=senMat.shape
        for individual in individualList:
            selectSenMat = []
            chromosome=individual.chromosome
            for i in chromosome:    #挑选对应染色体（传感器节点）上的敏感度矩阵的行组成新的压缩敏感度矩阵
                selectSenMat.append(senMat[i])
            selectSenMat=np.array(selectSenMat)
            result=0
            for i in range(leaks):  #计算个体适应度值
                temp=selectSenMat[:,i]
                if(i==leaks-1): #当在最后那列时不能继续再算
                    break
                for j in range(i+1,leaks):
                    result=result+temp.dot(selectSenMat[:,j])
            value=2*result/(leaks * (leaks - 1))
            individual.fitness=value    #这里需不需要需要考虑
            fitness.append(value)
        return fitness


    def selection(self,initPops,fitness):
        """
        @param initPops: 种群
        @param fitness:
        """
        pass

    def cross(self,initPops):
        pass

    def mutation(self,initPops):
        pass

    def best(self,fitness,Pops):
        """
        @param fitness: 适应度
        @param Pops: 种群
        @return: 最好个体所对应的适应度，个体（染色体为节点的索引从0开始）
        """
        best_value=np.max(fitness)
        index=np.where(fitness== best_value)
        best_individual=Pops.populations[index]
        return best_value,best_individual
    def resultPlot(self):
        pass

if __name__=="__main__":
    g=ga(10,2,0.8,0.1,500,"D:/科研/code/sensorLayout/result/Net3.inp")
    Pops = population(10, 2, "D:/科研/code/sensorLayout/result/Net3.inp")
    Pops.generatePopulations()  # 产生初始种群
    g.calFiteness(Pops,np.array(range(1,10)).reshape(3,3))















