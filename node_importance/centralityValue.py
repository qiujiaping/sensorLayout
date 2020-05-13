import wntr
import networkx as nx
import matplotlib.pyplot as plt

def get_centralityValue(filename):
    """
    @param filename: inp文件
    @return: 返回度，接近，介数，改进k-shell中心性
    """
    wn=wntr.network.WaterNetworkModel(filename)
    G = wn.get_graph()
    IKs=get_improve_kshell(G)
    Old_IKs_centrality={}
    for k,v in IKs.items():
        for nodeName in v:
            Old_IKs_centrality.update({nodeName:k})
    IKs_centrality = {}
    for nodeName in G.nodes():
        IKs_centrality[nodeName]=Old_IKs_centrality[nodeName]
    a=nx.degree_centrality(G)
    uG = G.to_undirected()  # undirected multigraph
    sG = nx.Graph(uG)   # undirected simple graph (single edge between two nodes)
    degree_centrality=nx.degree_centrality(G)#节点度
    betweenness_centrality = nx.betweenness_centrality(sG)#节点介数中心性
    closeness_centrality = nx.closeness_centrality(G)#节点中介中心性
    return degree_centrality,closeness_centrality,betweenness_centrality,IKs_centrality


def get_improve_kshell(G):
    """
    计算节点的改进k-shell值
    :param graph: 图
    :return: importance_dict{ks:[nodes]}
    """
    graph=G.copy()
    IKs = {}
    ks = 1
    #当递归删除所剩下的节点为0时则结束循环
    while graph.nodes():
        temp = []
        node_degrees_dict = graph.degree()
        minDegree= min(node_degrees_dict.values()) #找到剩下度最小的nodes
        for k, v in node_degrees_dict.items():
            if v == minDegree:
                temp.append(k)
                graph.remove_node(k)
        IKs[ks] = temp
        ks += 1
        node_degrees_dict = graph.degree()
    return IKs

if __name__=="__main__":
    filename="data/Net3.inp"
    get_centralityValue(filename)
