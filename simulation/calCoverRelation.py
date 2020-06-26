
# 得到各点覆盖节点情况(存储的是节点序号而非名称)
'''
@author: 雨夜微凉
@contact: 1475477624@qq.com
@file: simulation.py
@time:
@desc:
'''
import csv
import numpy as np
from random import  sample

def getCover(dFM_path):
    """
    获得每个节点所能覆盖的爆管节点
    @param dFM_path: 需求影响矩阵
    @return: 返回所有节点所能覆盖的爆管点[[]]
    """
    with open(dFM_path, 'r') as f:
        reader = csv.reader(f)
        demandFluMat = []
        for row in reader:
            demandFluMat.append(list(map(float, row)))
    demandFluMat=np.array(demandFluMat)

    allCoverRelation = {}
    for column in range(len(demandFluMat[0])):
        node_data=demandFluMat[:,column]
        index=np.where(node_data >0.7)[0]
        allCoverRelation.update({column:index})
    return allCoverRelation

def calCover(monitors,allCoverRelation):
    """

    @param monitors: 监测点对应为染色体/个体
    @param allCoverRelation: 所有节点的覆盖关系
    @return: 个体所覆盖的爆管点
    """
    coverNodes=[]
    for nodeIndex in monitors:
        coverNodes.extend(allCoverRelation[nodeIndex])
    coverNodes=list(set(coverNodes))
    return coverNodes

if __name__ == '__main__':
    allCoverNodes=getCover(r"D:\科研\code\sensorLayout\result\Net3\dFM.csv")
    monitors=sample(range(92),10)
    calCover(monitors,allCoverNodes)

    # #getCover("Net3_leakSensi.csv")
    #
    # monitors=['J-617', 'J-993', 'J-794', 'J-732', 'J-1057', 'J-810', 'J-285', 'J-331', 'J-632', 'J-1247', 'J-1123', 'J-736', 'J-946', 'J-42', 'J-1162', 'J-392', 'J-721', 'J-227', 'J-1278', 'J-730', 'J-704', 'J-772', 'J-998', 'J-393', 'J-509', 'J-327', 'J-806', 'J-324', 'J-1260', 'J-180', 'J-95', 'J-1280', 'J-683', 'J-192', 'J-1221', 'J-898', 'J-895', 'J-1118', 'J-111', 'J-13', 'J-1099', 'J-57', 'J-1041', 'J-497', 'J-864', 'J-789', 'J-656', 'J-1218', 'J-758', 'J-1226']
    # num=calCover("nodesKy8.csv",allCoverNodes,monitors)
    # print(num)
