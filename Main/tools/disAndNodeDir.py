import wntr
import numpy as np
import json
import os
import networkx as nx

"""
该模块是计算节点距离
"""
class distance_nodeDir:
    def __init__(self,inp):
        self.inp=inp
    def geo_distance(self,is_save=False,save_path=r'D:/科研/code/sensorLayout/result'):
        origiName = os.path.split(os.path.realpath(self.inp))[1].split(".")[0]
        wn = wntr.network.WaterNetworkModel(self.inp)
        nodeIds=wn.junction_name_list # ['10', '15', '20'....
        nodeIdAndIndex={}             # {'10': 0, '15': 1, '20': 2, '35': 3,......
        length=len(nodeIds)
        for i in range(length):
            nodeIdAndIndex.update({nodeIds[i]:i})
        nodeDisDic={} #{节点1：{节点2：距离，...节点n：距离}，....节点m：{节点m+1：距离，...节点n：距离}}
        disMat=np.zeros((length,length))
        for id in nodeIds:
            junction1=wn.get_node(id)
            index=nodeIdAndIndex[id]
            # if((index+1)==len(nodeIds)):
            #     break
            temp = {} #id节点和其他节点之间的距离{其他节点：距离}
            for i in range(index,len(nodeIds)):  #只算上三角形，减少一半计算量
                key=nodeIds[i]
                junction2=wn.get_node(key)
                coor1=np.array(junction1.coordinates)
                coor2=np.array(junction2.coordinates)
                dis=np.sqrt(sum((coor2-coor1)**2)) #计算节点距离
                disMat[i][index]=disMat[index][i]=dis
                temp.update({key:dis})
            nodeDisDic.update({id:temp})
        if(is_save==True):
            json_str = json.dumps(nodeDisDic, ensure_ascii=False, indent=4) #ensure_ascii = False(输出中文)， indent = 4(缩进为4)
            origiName = os.path.split(os.path.realpath(self.inp))[1].split(".")[0]
            with open(save_path+"/%s"%origiName+'/%sgeoDisDic.json'%origiName, 'w', encoding='utf-8') as f:
                f.write(json_str)
        # return nodeDisDic,disMat
        return disMat

    def topo_distance(self,is_save=False,save_path=r"D:/科研/code/sensorLayout/result"):
        wn = wntr.network.WaterNetworkModel(self.inp)
        nodeID=wn.junction_name_list
        row=wn.num_junctions
        G = wn.get_graph()
        sG = nx.Graph(G)
        p = dict(nx.shortest_path_length(sG))
        topo_distance=np.zeros(shape=(row,row))
        row=0
        for key1 in nodeID:
            column=0
            for key2 in nodeID:
                topo_distance[row][column]=p.get(key1).get(key2)
                column = column+1
            row=row+1
        if(is_save==True):
            origiName = os.path.split(os.path.realpath(self.inp))[1].split(".")[0]
            topo_distanceFileName = save_path+"/%s"%origiName+"/%stopo_distanceMat.csv"%origiName
            np.savetxt(topo_distanceFileName,topo_distance, delimiter=',')
        return topo_distance

    def get_nodeIndexId(self):
        wn = wntr.network.WaterNetworkModel(self.inp)
        nodeID = wn.junction_name_list
        nodeIndexId = {}
        for i in range(len(nodeID)):
            nodeIndexId.update({i: nodeID[i]})
        return nodeIndexId


if __name__=="__main__":
    inp = "D:/project/Cpp/data/Net3.inp"
    dn=distance_nodeDir(inp)
    # dis.geo_distance(is_save=True)
    # dis.topo_distance(is_save=True)
    print(dn.get_nodeIndexId())


