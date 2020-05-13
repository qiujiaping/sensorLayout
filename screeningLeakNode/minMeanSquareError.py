import wntr
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import math
from wntr.network import WaterNetworkModel

"""
用于指标筛选，把均方差很小的指标去除
"""

def getNode24hValue(inpFile):
    # 产生水力模型wn
    wn= wntr.network.WaterNetworkModel(inpFile)
    # 输入数据利用水力求解器进行水力计算
    sim=wntr.sim.EpanetSimulator(wn)
    results=sim.run_sim()
    # node_keys = results.node.keys() ['demand', 'head', 'pressure', 'quality'],通过该函数可以获得节点结果包含哪些属性
    pressure=results.node["pressure"]
    print(pressure)
    demand = results.node["demand"]
    pressureIndex=[]
    demandIndex = []
    for nodeId in wn.node_name_list:
        pressureIndex.append(pressure.loc[:,nodeId].values)
        demandIndex.append(demand.loc[:,nodeId].values)
    pressureStd=[]
    pressureMax=[]
    for node24hPre in pressureIndex:
        pressureStd.append(np.std(node24hPre))
        pressureMax.append(np.max(node24hPre))
    demandMax=[]
    for node24hDem in demandIndex:
        demandMax.append(np.max(node24hDem/(0.003785411784/60)))
    return pressureStd,pressureMax,demandMax


def getNodeDegree(inpFile):
    wn = wntr.network.WaterNetworkModel(inpFile)
    G = wn.get_graph()  # directed multigraph
    degreeIndex=[]
    for nodeId in wn.node_name_list:
        degreeIndex.append(G.degree(nodeId))
    return degreeIndex

"""
获得节点关联管道的长度和直径
"""
def getNodeDiaAndLen(inpFile):
    wn = wntr.network.WaterNetworkModel(inpFile)
    node_link={}
    for node_name in wn.node_name_list:
        node_link.update({node_name:wn.get_links_for_node(node_name)})
    node_linkLength={}
    node_linkDiameter={}
    # print(node_link)
    for key in node_link.keys():
        length=[]
        diameter=[]
        for pipId in wn.get_links_for_node(key):
            # Pump被当作管道link
            if(isinstance(wn.get_link(pipId),wntr.network.elements.Pipe)):
                # 记录与节点关联的每根管道的直径和长度(单位国际制)
                diameter.append(wn.get_link(pipId).diameter*1000/25.4)
                length.append(wn.get_link(pipId).length / 0.3048)
        node_linkLength.update({key:length})
        node_linkDiameter.update({key:diameter})

    return node_linkLength,node_linkDiameter

def getNodeToLenAndMinDia(inpFile):
    node_linkLength,node_linkDiameter=getNodeDiaAndLen(inpFile)
    print(node_linkDiameter)
    node_totalLength = []
    for value in node_linkLength.values():
        node_totalLength.append(np.sum(value))

    node_MinDiameter = []  # 每个节点关联的最小直径
    for value in node_linkDiameter.values():
        if (len(value) > 0):
            node_MinDiameter.append(1/np.min(value))
        else:
            node_MinDiameter.append(444444)     #需要将node_MinDiameter预处理转换为
    return node_totalLength,node_MinDiameter

def getNodeVolume(inpFile):
    node_linkLength,node_linkDiameter=getNodeDiaAndLen(inpFile)
    volume=[]
    area=[]
    length=list(node_linkLength.values())
    for value in node_linkDiameter.values():
        area.append([math.pi*math.pow(dia/2,2) for dia in value])
    for i in range(len(length)):
        volume.append(list(np.multiply(length[i], area[i])))
    totalVolume = []
    for item in volume:
        totalVolume.append(sum(item))
    nodeTotalVolume=dict(zip(node_linkLength.keys(),totalVolume))
    totalVolume=[]
    for value in nodeTotalVolume.values():
        totalVolume.append(value)
    return totalVolume


def getAllIndSME(inpFile):
    """
    获得节点压力均方差，最大压力，需求最大，节点的度数，关联的总管长，最小直径，关联的管段总体积7个指标
    """
    IndicatorStd=[]  #存放每个指标的样本均方差
    pressureStd,pressureMax,demandMax=getNode24hValue(inpFile)  #获得每个节点的压力均方差，最大压力，需求最大
    degreeIndex=getNodeDegree(inpFile)  #获得每个节点的度数
    node_totalLength,node_MinDiameter=getNodeToLenAndMinDia(inpFile)    #获得节点关联的总管长，最小直径
    # print()
    nodeTotalVolume=getNodeVolume(inpFile)  #获得每个节点关联的管段总体积
    IndicatorStd.append(np.std(pressureStd[0:92]))
    IndicatorStd.append(np.std(pressureMax[0:92]))
    IndicatorStd.append(np.std(demandMax[0:92]))
    IndicatorStd.append(np.std(degreeIndex[0:92]))
    IndicatorStd.append(np.std(node_totalLength[0:92]))
    IndicatorStd.append(np.std(node_MinDiameter[0:92]))
    IndicatorStd.append(np.std(nodeTotalVolume[0:92]))
    print(IndicatorStd)
    return IndicatorStd

def drawPlot(inpFile):
    pressureStd, pressureMax, demandMax = getNode24hValue(inpFile)  # 获得每个节点的压力均方差，最大压力，需求最大
    degreeIndex = getNodeDegree(inpFile)  # 获得每个节点的度数
    node_totalLength, node_MinDiameter = getNodeToLenAndMinDia(inpFile)  # 获得节点关联的总管长，最小直径
    nodeTotalVolume = getNodeVolume(inpFile)  # 获得每个节点关联的管段总体积
    plt.subplot(331)
    plt.plot(list(range(92)), pressureStd[0:92], 'b-.')
    plt.title('pressureStd')
    plt.subplot(332)
    plt.plot(list(range(92)), pressureMax[0:92], 'b-.')
    plt.title('pressureMax')
    plt.subplot(333)
    plt.plot(list(range(92)), demandMax[0:92], 'b-.')
    plt.title('demandMax')
    plt.subplot(334)
    plt.plot(list(range(92)), degreeIndex[0:92], 'b-.')
    plt.title('degreeIndex')
    plt.subplot(335)
    plt.plot(list(range(92)), node_totalLength[0:92], 'b-.')
    plt.title('node_totalLength')
    plt.subplot(336)
    plt.plot(list(range(92)), node_MinDiameter[0:92], 'b-.')
    plt.title('node_MinDiameter')
    plt.subplot(337)
    plt.plot(list(range(92)), nodeTotalVolume[0:92], 'b-.')
    plt.title('nodeTotalVolume')
    plt.tight_layout()
    plt.show()

def getAllData(inpFile):
    data=[]
    pressureStd, pressureMax, demandMax = getNode24hValue(inpFile)  # 获得每个节点的压力均方差，最大压力，需求最大
    degreeIndex = getNodeDegree(inpFile)  # 获得每个节点的度数
    node_totalLength, node_MinDiameter = getNodeToLenAndMinDia(inpFile)  # 获得节点关联的总管长，最小直径
    nodeTotalVolume = getNodeVolume(inpFile)  # 获得每个节点关联的管段总体积
    data.append(pressureStd)
    data.append(pressureMax)
    data.append(demandMax)
    data.append(degreeIndex)
    data.append(node_totalLength)
    data.append(node_MinDiameter)
    data.append(nodeTotalVolume)
    return data

if __name__=="__main__":
    """
    此模块把数据获取包括：
     1.每个节点24小时的压力（最大压力，方差）
     2.每个节点24小时的流量（最大流量）
     3.每个节点的度数
     4.每个节点的平均管径
     5.每个节点的管径极差
     6.每个节点的管长
      ft=0.3048m
      1GPM=0.003785411784/60.0m3/s
      1in=25.4毫米
      wn.get_node('101').base_demand/(0.003785411784/60.0)获得节点基本需求，查阅wntr.network.elements module
    """
    getNode24hValue("data/ky8.inp")
    # getNodeVolume("data/Net3.inp")
    # getAllIndSME("data/Net3.inp")
    # getNodeToLenAndMinDia("data/Net3.inp")


