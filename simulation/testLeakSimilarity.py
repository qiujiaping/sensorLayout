#!/usr/bin/env python
# encoding: utf-8
'''
@author: 雨夜微凉
@contact: 1475477624@qq.com
@file: testLeakSimilarity.py
@time: 2020/5/9 20:10
@desc:这里可视化的是节点真实泄漏和其他泄漏的相似性对比，这里是硬编码的形式，需要改变
'''
from Mat import Data
from readAndDraw import loadSensitiveMat
import random
import numpy as np
import wntr
from matplotlib import cm
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def drawAllTest(inp):
    """
        测试完备观测状态下的泄漏相似性
    @param inp:
    @param dotProduct:
    """
    origMat = loadSensitiveMat("result/Net3.csv")
    leaks, n = origMat.shape
    # random.seed(1)
    # randomLeak = random.randint(0, leaks - 1)

    # 取索引为[]的节点（从0开始）泄漏点
    leakVector = origMat[63]
    mat = origMat.T
    dotProduct = leakVector.dot(mat)
    wn=wntr.network.WaterNetworkModel(inp)
    nodes=wn.node_name_list
    dotProductDic={}
    index=0
    for nodeId in nodes:
        try:
            dotProductDic.update({nodeId:dotProduct[index]})
            index=index+1
        except:
            for i in range(92,97):
                dotProductDic.update({nodes[i]:0})
    wntr.graphics.plot_network(wn, node_attribute=dotProductDic, title="漏损相似性", node_size=30,node_cmap=cm.coolwarm)
    plt.show()

def drawSampleTest(inp,value):
    """
        测试降维（压缩）状态下的泄漏相似性
    @param inp:
    @param dotProduct:
    """
    origMat = loadSensitiveMat("D:/科研/code/sensorLayout/result/ky8.csv")
    mat=origMat.T
    # random.seed(value)
    sensors=np.sort(random.sample(range(1325),25))
    measureMat=[]
    for i in range(len(sensors)):
        nodeIndex=sensors[i]
        measureMat.append(mat[nodeIndex])
    measureMat=np.array(measureMat).T
    measureMat=np.array([row / np.linalg.norm(row) for row in measureMat]).T #单位化
    leakVector=measureMat.T[63]
    dotProduct = leakVector.dot(measureMat) #降维的相似泄漏内积
    #以上求内积，以下可视化
    wn=wntr.network.WaterNetworkModel(inp)
    nodes=wn.node_name_list
    dotProductDic={}
    index=0
    for nodeId in nodes:
        try:
            dotProductDic.update({nodeId:dotProduct[index]})
            index=index+1
        except:
            for i in range(92,97):
                dotProductDic.update({nodes[i]:0})
    wntr.graphics.plot_network(wn, node_attribute=dotProductDic, title="漏损相似性", node_size=30,node_cmap=cm.coolwarm)
    plt.show()
    print("1")

if __name__=="__main__":
    # drawAllTest("result/Net3.inp")
    # sensors = np.sort(random.sample(range(92), 6))
    # print(sensors)
    # a=np.array(range(12)).reshape(3,4)
    # print(a)
    # drawAllTest("result/Net3.inp")
    # for i in range(92):
    drawSampleTest("D:/科研/code/sensorLayout/result/ky8.inp",0)







