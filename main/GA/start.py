#!/usr/bin/env python
# encoding: utf-8
from main.GA.population import population
import numpy as np
from simulation.readAndDraw import loadSensitiveMat
import wntr
import matplotlib.pyplot as plt
import time
import random
from copy import copy

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
    def run(self,senMat):
        """
        @param senMat: 敏感度矩阵
        """
        senMat=senMat.T #转置使得行为节点，列为泄漏点

        Pops=population(self.pop_size,self.chrom_length,self.inp)
        Pops.initPopulations()   #产生初始种群
        for  i in range(self.iteration):
            start = time.clock()
            fitness=self.calFiteness(Pops,senMat)
            fitnessTime = time.clock()
            # print('适应度计算耗时%s' % (fitnessTime - start))
            best_value, best_individual = self.best(fitness, Pops)
            print(best_value,best_individual)
            self.eachGeneBestValue.append([best_value,best_individual]) #存放每一代最好的值
            self.selection(Pops,fitness)   #选择
            self.cross(Pops)               #交叉
            self.mutation(Pops)            #变异
            eachGeneTime=time.clock()
            print('第',i,'代计算耗时%s' % (eachGeneTime - start))
        with open("D:/科研/code/sensorLayout/result/Net3.txt",'w')as f:
            f.write(str(self.eachGeneBestValue))


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
                # 单位化,为了计算方便不用在分母处除模
                unitTemp1= temp/np.linalg.norm(temp)
                if(i==leaks-1): #当在最后那列时不能继续再算
                    break
                for j in range(i+1,leaks):
                    temp2=selectSenMat[:,j]
                    unitTemp2=temp2/np.linalg.norm(temp2)
                    result=result+unitTemp1.dot(unitTemp2)
            value=2*result/(leaks * (leaks - 1))
            individual.fitness=value    #这里需不需要需要考虑
            fitness.append(value)
        return fitness


    def selection(self,initPops,fitness):
        """

            《《《《《《《《可能改为锦标赛选择可能更好

        @param initPops: 种群
        @param fitness:
        """
        new_fitness=[1-value for value in fitness]  #使得越小的越大，方便计算
        total_fitness=sum(new_fitness)
        single_p_list=[value/total_fitness for value in new_fitness]
        temp_sum=0
        P = []
        for p in single_p_list:
            temp_sum=temp_sum+p
            P.append(temp_sum)
        dice=[]
        length=len(fitness)
        for i in range(length):  # 预先转好轮盘
            dice.append(random.random())
        dice.sort()
        new_chromosomes=[]
        num_in=0    #新选择的个体数
        cursor=0    #游标，若当前筛子的概率大于游标所指轮盘的概率则游标向前滑动以扩大范围

        #选择
        while num_in<length:
            if(dice[num_in]<=P[cursor]):
                new_chromosomes.append(initPops.populations[cursor].chromosome)
                num_in=num_in+1
            else:
                cursor=cursor+1
        # 选择的赋给种群
        changeIndex=0
        for individual in initPops.populations:
            individual.chromosome=new_chromosomes[changeIndex]
            changeIndex=changeIndex+1


    def cross(self,pops):
        """
        交叉
        @param pops: 种群
        """
        old_population = copy(pops.populations)
        for i in range(self.pop_size- 1):
            r=random.random()
            if r < self.pc:
                crossPoint = self.chrom_length// 2
                for n in range(crossPoint, self.chrom_length):  # 选择是在个体一半处进行交叉,交换两个个体的后半段
                    mid = pops.populations[i].chromosome[n]
                    pops.populations[i].chromosome[n] = pops.populations[i+1].chromosome[n]
                    pops.populations[i+1].chromosome[n] = mid
        for i in range(self.pop_size):
            length= len(set(pops.populations[i].chromosome))
            if length < self.chrom_length:
                pops.populations[i].chromosome = old_population[i].chromosome

    def mutation(self,pops):
        old_population = copy(pops.populations) #获得个体对象列表
        for i in range(self.pop_size):
            r = random.random()
            n = random.randint(0, self.chrom_length // 2)  # 在个体的前半段随机选取一个点进行变异
            m = random.randint(self.chrom_length // 2, self.chrom_length - 1)  # 在个体的后半段随机选取一个点进行变异
            if r <= self.pm:
                if pops.populations[i].chromosome[n]+1<=pops.nodeIndexList[-1]:
                    pops.populations[i].chromosome[n] = pops.populations[i].chromosome[n]+1  # 整数编码,随机+1或者减1
                if pops.populations[i].chromosome[m]-1 >= 0:
                    pops.populations[i].chromosome[m] = pops.populations[i].chromosome[m]- 1
        for i in range(self.pop_size):
            length= len(set(pops.populations[i].chromosome))
            if length < self.chrom_length:
                # print(population[i],old_population[i])
                pops.populations[i].chromosome = old_population[i].chromosome


    def best(self,fitness,Pops):
            """
            @param fitness: 适应度
            @param Pops: 种群
            @return: 最好个体所对应的适应度，个体（染色体为节点的索引从0开始）
            """
            best_value=np.min(fitness)
            index=np.where(fitness== best_value)    #index为元组类型这里提取第一个元素
            best_individual=copy(Pops.populations[index[0][0]].chromosome)
            return best_value,best_individual


    def resultPlot(self):
        pass


if __name__=="__main__":
    g=ga(100,12,0.6,0.1,3,"D:/科研/code/sensorLayout/result/Net3.inp")
    unitMat=loadSensitiveMat("D:/科研/code/sensorLayout/result/Net3.csv")
    g.run(unitMat)


















