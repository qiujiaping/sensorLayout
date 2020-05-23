import wntr
import numpy as np
import json
import os

"""
该模块是计算节点距离
"""
def distance(inp):
    origiName = os.path.split(os.path.realpath(inp))[1].split(".")[0]
    wn = wntr.network.WaterNetworkModel(inp)
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
    json_str = json.dumps(nodeDisDic, ensure_ascii=False, indent=4) #ensure_ascii = False(输出中文)， indent = 4(缩进为4)
    with open('D:/科研/code/sensorLayout/result/%sDisDic.json'%origiName, 'w', encoding='utf-8') as f:
        f.write(json_str)
    # return nodeDisDic,disMat
    return disMat



if __name__=="__main__":
    inp = "D:/project/Cpp/data/Net3.inp"
    distance(inp)