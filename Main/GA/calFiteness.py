#!/usr/bin/env python
# encoding: utf-8
import numpy as np
'''
@author: 雨夜微凉
@contact: 1475477624@qq.com
@file: calFiteness.py
@time: 2020/5/23 19:02
@desc:计算适应度
'''

def calFiteness(Pops,disMat,senMat:np.ndarray):
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
        # prMat=np.zeros((leaks,leaks))
        for i in range(leaks):  #计算个体适应度值,这里有bug,可能np.linalg.norm(temp)=0
            temp=selectSenMat[:,i]
            # 单位化,为了计算方便不用在分母处除模
            unitTemp1= temp/np.linalg.norm(temp)
            if(i==leaks-1): #当在最后那列时不能继续再算
                break
            for j in range(i+1,leaks):
                temp2=selectSenMat[:,j]
                unitTemp2=temp2/np.linalg.norm(temp2)
                dotProduct=unitTemp1.dot(unitTemp2)
                # prMat[i][j]=dotProduct
                # prMat[j][i] =dotProduct
                # if(i!=j):
                result=result+dotProduct
        value=2*result/(leaks * (leaks - 1))
        # 根据距离矩阵和相似度字典求距离更改适应度
        # similarDir={i:[] for i in range(leaks)}
        # for i in range(leaks):
        #     for j in range(i,leaks):
        #         if(prMat[i][j]>value and i!=j):
        #             similarDir[i].append(j)
        #             similarDir[j].append(i)
        # disSum=0
        # for i in range(leaks):
        #     tempDisMax=0
        #     for j in similarDir[i]:
        #         if(disMat[i][j]>tempDisMax):
        #             tempDisMax=disMat[i][j]
        #     disSum=disSum+tempDisMax
        # avlDis=disSum/(leaks)
        fitness.update({chromosome_index:value})
        chromosome_index=chromosome_index+1
    fitness = sorted(fitness.items(), key=lambda item: item[1])
    new_fitness={}
    for index_value in fitness:
        new_fitness.update({index_value[0]:index_value[1]})
    return new_fitness

