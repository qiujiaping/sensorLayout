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
        self.eachGeneBestValue={} #存放每一代最好值[[适应度，个体]]
        self.inp=inp
        wn=wntr.network.WaterNetworkModel(inp)
        nodeID=wn.junction_name_list
        self.nodeIdIndex={}
        for i in range(len(nodeID)):
            self.nodeIdIndex.update({nodeID[i]:i})
        self.nodeIndexList = list(range(len(nodeID)))  # 节点id范围

    """
        ga算法的启动函数
    """
    def run(self,senMat):
        """
        @param senMat: 敏感度矩阵
        """
        senMat=senMat.T #转置使得行为节点，列为泄漏点
        Pops=population(self.pop_size,self.chrom_length,self.inp)
        fitness= self.calFiteness(Pops, senMat)
        start = time.clock()
        for  i in range(self.iteration):
            # 复制一份父代
            parents=Pops.copy()
            # 记录该代最好的
            values=list(fitness.values())
            keys=list(fitness.keys())
            print(values[0])
            self.eachGeneBestValue.update({values[0]:Pops[keys[0]]}) #存放每一代最好的值

            #产生子代
            childs=self.selection(Pops,fitness)   #选择
            self.cross(childs)               #交叉
            self.mutation(childs)            #变异

            # 子代和父代混合，选取前一半最好适应度的个体（精英保留策略）
            parents_childs= np.vstack((parents, childs))
            fitness={}
            Pops = []
            index=0
            for key,value in list(self.calFiteness(parents_childs,senMat).items())[:self.pop_size]:
                fitness.update({index:value})
                Pops.append(parents_childs[key])
                index=index+1
            end = time.clock()
        print(end-start)
        self.resultPlot()

    """
    计算适应度
    """
    def calFiteness(self,Pops,senMat:np.ndarray):
        """
        @param initPops: 种群
        @param senMat: 敏感度矩阵senMat.shape=[n，leaks]
        @return: 适应度(每个个体的平均互相干系数)字典，节点索引：适应度
        """
        fitness={}
        n,leaks=senMat.shape
        chromosome_index = 0
        for indivi in Pops:
            selectSenMat = []
            for i in indivi:    #挑选对应染色体（传感器节点）上的敏感度矩阵的行组成新的压缩敏感度矩阵
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
            fitness.update({chromosome_index:value})
            chromosome_index=chromosome_index+1
        fitness = sorted(fitness.items(), key=lambda item: item[1])
        new_fitness={}
        for index_value in fitness:
            new_fitness.update({index_value[0]:index_value[1]})
        return new_fitness


    def selection(self,initPops,fitness):
        """

            《《《《《《《《可能改为锦标赛选择可能更好

        @param initPops: 种群数组
        @param fitness:
        """
        new_fitness=[1-value for value in fitness.values()]  #使得越小的越大，方便计算
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
        new_chromosomes=[]  #保存选择的个体的染色体
        temp_fitness=[]     #保存选择的个体的适应度
        num_in=0    #新选择的个体数
        cursor=0    #游标，若当前筛子的概率大于游标所指轮盘的概率则游标向前滑动以扩大范围
        keys=list(fitness.keys())
        values=list(fitness.values())
        #选择
        while num_in<length:
            if(dice[num_in]<=P[cursor]):
                new_chromosomes.append(initPops[keys[cursor]])
                temp_fitness.append(values[cursor])
                num_in=num_in+1
            else:
                cursor=cursor+1
        return new_chromosomes


    def cross(self,pops):
        """
        交叉
        @param pops: 种群
        """
        old_chromosome =pops.copy()
        for i in range(self.pop_size- 1):
            r=random.random()
            if r < self.pc:
                crossPoint = self.chrom_length// 2
                for n in range(crossPoint, self.chrom_length):  # 选择是在个体一半处进行交叉,交换两个个体的后半段
                    mid = pops[i][n]
                    pops[i][n]= pops[i+1][n]
                    pops[i+1][n] = mid
        for i in range(self.pop_size):
            length= len(set(pops[i]))
            if length < self.chrom_length:
                pops[i] = old_chromosome[i]

    def mutation(self,pops):
        old_chromosome = pops.copy()
        for i in range(self.pop_size):
            r = random.random()
            n = random.randint(0, self.chrom_length // 2)  # 在个体的前半段随机选取一个点进行变异
            m = random.randint(self.chrom_length // 2, self.chrom_length - 1)  # 在个体的后半段随机选取一个点进行变异
            if r <= self.pm:
                if pops[i][n]+1<=self.nodeIndexList[-1]:
                    pops[i][n] = pops[i][n]+1  # 整数编码,随机+1或者减1
                if pops[i][m]-1 >= 0:
                    pops[i][m] = pops[i][m]- 1
        for i in range(self.pop_size):
            length= len(set(pops[i]))
            if length < self.chrom_length:
                # print(population[i],old_population[i])
                pops[i] = old_chromosome[i]


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


    def resultPlot(self):

        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        # 在坐标轴上显示节点重要性图
        plt.plot(range(len(self.eachGeneBestValue.keys())), [fiteness for fiteness in self.eachGeneBestValue.keys()], marker="o", label="节点号-重要性图")
        # plt.xticks(range(self.iteration), range(self.iteration), rotation=90)
        plt.xlabel('代数')
        plt.ylabel("平均互相干系数")
        plt.show()


if __name__=="__main__":
    g=ga(100,6,0.6,0.1,300,"D:/科研/code/sensorLayout/result/Net3.inp")
    unitMat=loadSensitiveMat("D:/科研/code/sensorLayout/result/Net3.csv")
    g.run(unitMat)


















