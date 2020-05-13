from centralityValue import get_centralityValue
from AHP import ahp
import numpy as np
import matplotlib.pyplot as plt
import wntr

"""
该模块是计算网络的节点重要性
"""


plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False
def get_AttrMat(filename):
    """
    @param filename: 输入inp文件路径
    @return: 标准的属性矩阵，未带权
    """
    centralityList=get_centralityValue(filename)#分别放4个属性的样本
    attributeMatrix=[]
    for item in centralityList:
        temp=[]
        for v in item.values():
            temp.append(v)
        attributeMatrix.append(temp)
    attributeMatrix=np.array(attributeMatrix)
    stand_attributeMatrix=[]
    for item in attributeMatrix:
        tempSum=np.power(np.sum(np.power(item, 2)),0.5)
        tempList=[]
        for v in item:
            tempList.append(v/tempSum)
        stand_attributeMatrix.append(tempList)
    stand_attributeMatrix=np.array(stand_attributeMatrix)
    return stand_attributeMatrix

def get_WithWeiAttrMat(inpFile,ahp_filename):
    """
    @param inpFile:
    @param ahp_filename:
    @return 返回带权属性矩阵,行代表样本，列代表属性（Net3 则为97*4）
    """
    stand_attributeMatrix=get_AttrMat(inpFile)
    weight=ahp(ahp_filename)
    print(weight)
    withWeiAttrMat=np.multiply(stand_attributeMatrix.T,weight)
    return withWeiAttrMat

def topsis(withWeiAttrMat):
    """
    @param withWeiAttrMat:
    @return 返回各节点的重要性
    """
    #确定正负理想对象
    A_pos=withWeiAttrMat.max(axis=0)
    A_neg=withWeiAttrMat.min(axis=0)
    #计算距离
    S_pos=np.power(np.sum(np.power(withWeiAttrMat-A_pos, 2), axis=1),0.5)   #样本与正理想对象的距离
    S_neg=np.power(np.sum(np.power(withWeiAttrMat-A_neg, 2), axis=1), 0.5)  #样本与负理想对象的距离
    #计算接近度
    Den=S_pos+S_neg
    importance=np.true_divide(S_neg,Den)
    # importance=np.sort(importance)  #按大小排好序
    return importance

def get_importance_dict(inpFile,importance):
    """
    @param inpFile: inp文件路径
    @param importance: 节点重要性
    @return: 节点重要性列表
    """
    wn=wntr.network.WaterNetworkModel(inpFile)
    nodes=wn.nodes
    importance_dict=dict(zip(nodes,importance))
    importance_list=sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)
    keys=[i[0] for i in importance_list]
    #在网络显示节点重要性图和坐标轴上显示
    wntr.graphics.plot_network(wn, node_attribute=importance_dict, title="节点重要性", node_size=30,node_labels=True,node_alpha=6)
    plt.show()
    #在坐标轴上显示节点重要性图
    plt.plot(range(len(importance_list)), [i[1] for i in importance_list],marker ="o",label="节点号-重要性图")
    plt.xticks(range(len(keys)),keys,rotation=90)
    plt.xlabel('节点编号')
    plt.ylabel("节点重要性")
    plt.legend()
    plt.show()
    return importance_dict

if __name__=="__main__":
    inpFile="data/Net3.inp"
    # inpFile = "data/ky8.inp"
    ahp_File="data/data.txt"
    withWeiAttrMat=get_WithWeiAttrMat(inpFile,ahp_File)
    importance=topsis(withWeiAttrMat)
    importance_dict=get_importance_dict(inpFile, importance)




