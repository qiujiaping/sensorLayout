from minMeanSquareError import getAllData
import numpy as np
import matplotlib.pyplot as plt
import wntr
import os
# from demo import getAllData

def getStData(inpFile):
    """
    获得数据
    """
    # sli=92
    sli=1317
    data=getAllData(inpFile) #一致化已经完成，需要无量纲化（标准化，规范化）
    stData=[]
    for item in data:
        item=item[0:sli]
        maxData=np.max(item)
        minData=np.min(item)
        item=[(i-minData)/(maxData-minData) for i in item]
        stData.append(item)
        A = np.array(stData) #行代表所有样本的一个指标的数据，列代表一个样本每个指标的数据
    return A

def getWeight(inpFile):
    """
    获得权值
    """
    A=getStData(inpFile)
    np.set_printoptions(suppress=True)
    H=np.dot(A,A.T)
    Eigenvalues,Eigenvector=np.linalg.eig(H)
    print(Eigenvector)
    staWeight=Eigenvector[:,0] #标准化的特征向量
    total=np.sum(staWeight)
    newWeight=[i/total for i in staWeight] #归一化
    norWeight=np.array(newWeight)
    return norWeight

def buildResult(inpFile):
    """
    @param inpFile:
    @return: 从大到小排列的所有节点的概率，排序后的所有节点ID，高于平均值的概率（排在平均值前面的节点概率）
    """
    slic=1317
    # slic = 92
    norWeight=getWeight(inpFile)
    print(norWeight)
    wn=wntr.network.WaterNetworkModel(inpFile)
    nodeId=wn.node_name_list
    A = getStData(inpFile)
    result=np.matmul(A.T,norWeight)
    nodeValue=dict(zip(nodeId[0:slic], result))
    nodeValue=sorted(nodeValue.items(), key=lambda x: x[1], reverse=True)
    sortedNodeID = []
    pickNodeValue = []
    for i in nodeValue:
        sortedNodeID.append(i[0])
        pickNodeValue.extend([i[1]])
    pickNodeValue = np.array(pickNodeValue)
    probability = 1. / (1. + np.exp(-pickNodeValue))
    probability = probability.tolist()
    pickBrustNodeP = [i for i in probability if i > np.mean(probability)]
    os.remove("temp.bin")
    os.remove("temp.inp")
    os.remove("temp.rpt")
    return probability,sortedNodeID,pickBrustNodeP

def drawResult(inpFile):
    wn = wntr.network.WaterNetworkModel(inpFile)
    probability,sortedNodeID,pickBrustNodeP=buildResult(inpFile)
    x=range(len(probability))
    plt.plot(x, probability)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    print(len(pickBrustNodeP))
    print(sortedNodeID[0:len(pickBrustNodeP)])
    wntr.graphics.plot_network(wn, node_attribute=sortedNodeID[0:len(pickBrustNodeP)], title="筛选爆管点结果", node_size=20)
    plt.show()

if __name__=="__main__":
    drawResult("data/ky8.inp")



