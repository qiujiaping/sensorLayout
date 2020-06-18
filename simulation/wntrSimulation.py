#!/usr/bin/env python
# encoding: utf-8
'''
@author: 雨夜微凉
@contact: 1475477624@qq.com
@file: simulation.py
@time:
@desc:
'''
import wntr
import matplotlib.pyplot as plt
import numpy as np
import random
import os

class HydraulicSimulation:
    """
        水力模拟类
        主要功能:
        多节点泄漏模拟
    """

    def __init__(self,inp_file):
        self.inp_file=inp_file
        self.wn = wntr.network.WaterNetworkModel(self.inp_file)
        self.nodeId = self.wn.junction_name_list  # 只在管网的连接节点上进行模拟
        self.nodeIndexId=self._getNodeIndexId(self.nodeId)
        self.nor_pressureAt0h=self._getNor_pressure(self.wn)

    def _getNodeIndexId(self,nodeId):
        nodeIndexId={}
        index=0
        for Id in nodeId:
            nodeIndexId.update({index: Id})
            index = index + 1
        return nodeIndexId

    def _getNor_pressure(self,wn):
        sim = wntr.sim.EpanetSimulator(wn)
        results = sim.run_sim()
        nor_pressureAt0h = np.array(results.node['pressure'].loc[0 * 3600, :])
        return nor_pressureAt0h

    def simLeakAll(self,leakFlow,is_save=True,save_path=r"D:\科研\code\sensorLayout\result"):
        pressureResidual=[]
        leak = wntr.epanet.util.to_si(wntr.epanet.util.FlowUnits.LPS, leakFlow,
                                           wntr.epanet.util.HydParam.Demand)  # 从L/s转到m³/s
        for nodeId in self.nodeId:
            wn = wntr.network.WaterNetworkModel(self.inp_file)
            junction = wn.get_node(nodeId)
            # 这里国际制是m³/s,1m³/s=1000L/s
            base_value = junction.demand_timeseries_list._list[0].base_value  # m³/s
            base_value_plus_leak = base_value + leak  # m³/s
            junction.demand_timeseries_list._list[0].base_value = base_value_plus_leak
            sim = wntr.sim.EpanetSimulator(wn)
            results = sim.run_sim()
            leak_pressure = np.array(results.node['pressure'].loc[0 * 3600, :])
            diff = self.nor_pressureAt0h - leak_pressure
            diff = wntr.epanet.util.from_si(wntr.epanet.util.FlowUnits.GPM, diff, wntr.epanet.util.HydParam.Pressure)
            pressureResidual.append(diff)
            if(is_save==True):
                origiName = os.path.split(os.path.realpath(inp_file))[1].split(".")[0]
                pressureResidualFileName = save_path+"/%s/"%origiName+"pr.csv"
                np.savetxt(pressureResidualFileName, pressureResidual, delimiter=',')
            os.remove("temp.bin")
            os.remove("temp.inp")
            os.remove("temp.rpt")
        return np.array(pressureResidual)
    # # <FlowUnits.GPM: (1, 6.30901964e-05)>
    # inp_file =r'Net3.inp'
    # a=[]
    # wn = wntr.network.WaterNetworkModel(inp_file)
    # sim = wntr.sim.EpanetSimulator(wn)
    # results = sim.run_sim()
    # nor_pressure=np.array(results.node['pressure'].loc[0*3600, :])
    # name_dir={}
    # index=0
    # for Id in wn.junction_name_list:
    #     name_dir.update({index:Id})
    #     index=index+1
    # for nodeName in wn.junction_name_list:
    #     wn = wntr.network.WaterNetworkModel(inp_file)
    #     junction = wn.get_node(nodeName)
    #     # 这里国际制是m³/s,1m³/s=1000L/s
    #     leak=wntr.epanet.util.to_si(wntr.epanet.util.FlowUnits.LPS,16.6,wntr.epanet.util.HydParam.Demand)#从L/s转到m³/s
    #     base_value=junction.demand_timeseries_list._list[0].base_value  #m³/s
    #     base_value_plus_leak=base_value+leak    #m³/s
    #     junction.demand_timeseries_list._list[0].base_value=base_value_plus_leak
    #     sim = wntr.sim.EpanetSimulator(wn)
    #     results = sim.run_sim()
    #     pressure=np.array(results.node['pressure'].loc[0*3600, :])
    #     diff=nor_pressure-pressure
    #     diff=wntr.epanet.util.from_si(wntr.epanet.util.FlowUnits.GPM, diff, wntr.epanet.util.HydParam.Pressure)
    #     a.append(diff)
    #     os.remove("temp.bin")
    #     os.remove("temp.inp")
    #     os.remove("temp.rpt")
    # pr2=np.zeros((len(a),len(a)))
    # pr1=np.zeros((len(a),len(a)))
    # for i in range(len(a)):
    #     random.seed(1)
    #     sam=np.sort(random.sample(range(92),5))
    #     b0=np.array(a[i])
    #     b = np.array(a[i])[sam]
    #     if(np.all(b==0)):
    #         pr2[i]=0
    #         pr2[i][i]=1
    #         pr1[i] = 0
    #         pr1[i][i] = 1
    #         continue
    #     unitTemp1 = b / np.linalg.norm(b)
    #     unitTemp0 = b0 / np.linalg.norm(b0)
    #     for j in range(i,len(a)):
    #         c0=np.array(a[j])
    #         c=np.array(a[j])[sam]
    #         if (np.all(c == 0)):
    #             pr2[i][j] = pr2[j][i]=0
    #             pr1[i][j] = pr1[j][i] = 0
    #             continue
    #         unitTemp2= c/np.linalg.norm(c)
    #         unitTemp3 = c0 / np.linalg.norm(c0)
    #         dotProduct0=unitTemp0.dot(unitTemp3)
    #         dotProduct=unitTemp1.dot(unitTemp2)
    #         pr2[i][j]=pr2[j][i]=dotProduct
    #         pr1[i][j] = pr1[j][i] = dotProduct0
    # print(pr)

if __name__=="__main__":
    inp_file=r"data\Net3.inp"

    hs=HydraulicSimulation(inp_file)
    pressureResidual=hs.simLeakAll(16.6,is_save=True)

    print()

