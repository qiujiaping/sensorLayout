#!/usr/bin/env python
# encoding:UTF-8
from Main.function.funModel import *
from itertools import chain

# 以下为具体实现函数
# 需要用户自定义函数，继承与上面的模板抽象函数
# 探测最大化，定位性能最大化
from simulation.calCoverRelation import *
class doubleMax(objectFun_2):
    def __init__(self, population, allCoverRelation,prMat,topo_distance,nodeIndexId,distance_threshold=15):
        """
        @param population: 种群
        @param allCoverRelation: 所有节点所能覆盖的爆管点的覆盖关系
        @param prMat: 残差矩阵/泄漏特征矩阵
        @param topo_distance: 拓扑距离
        @param nodeIndexId: 节点索引和节点ID字典
        @param distance_threshold: 拓扑距离阈值net3=7,ky2=15
        """
        objectFun_2.__init__(self, population)
        self.allCoverRelation=allCoverRelation
        self.prMat=prMat
        self.topo_distance = topo_distance
        self.nodeIndexId = nodeIndexId
        self.distance_threshold=distance_threshold#这里需要根据管网情况定义
        self.similarity=0.95

    def objFun_1_Max(self):
        """
        计算种群当中染色体的覆盖节点
        @return:1:每个个体能监测的爆管事件
                2:每个个体未监测泄漏的比例
        """
        pop_cover = []  #存放每个个体能监测的爆管事件
        monitored_ratio=[]#存放每个个体未监测泄漏的比例
        leak_num=len(self.prMat)
        for indivi in self.population:
            coverNodes=self.calCover(indivi)
            # monitored = len(coverNodes) /leak_num
            # monitored = float('%.3f' % monitored)
            monitored_ratio.append(len(coverNodes))
            pop_cover.append(coverNodes)
        return monitored_ratio,pop_cover


    def objFun_2_Max(self,pop_cover):
        """
        这个函数是用来评估定位性能的，放置一组监测点，考察其探测得到的泄漏节点在该集合上产生的
        泄漏特征与其它泄漏节点在该监测集合上产生相似特征的话，评估其泄漏节点和其他产生泄漏相似节点之间的距离
        如果超过给定的距离阈值则给惩罚，目的是使得产生相似泄漏特征节点在尽可能近的范围
        @param pop_cover: 种群中每个个体所能监测的泄漏节点
        @return：每个个体的定位性能（受到的惩罚比例）
        """
        #获取每个个体覆盖的爆管数据，并对应个体/监测点位置的数据，所有个体的所能检测到的爆管灵敏度数据存放到一个容器
        pop_cover_leak_data = []
        pop_pr=[]   #所有监测集合/个体对应残差矩阵里的列数据如92*10
        for i in range(len(pop_cover)):
            individual_coverLeaks=pop_cover[i]
            individual=self.population[i]
            pop_pr.append(self.prMat[:,individual])
            indivi_cover_leak_data = [] #个体所能监测泄漏对应残差矩阵里的列数据如59*10
            for leak_index in individual_coverLeaks:
                row_data=self.prMat[leak_index][individual]
                if(np.linalg.norm(row_data)!=0):
                    row_data=row_data/np.linalg.norm(row_data)
                indivi_cover_leak_data.append(row_data)
            pop_cover_leak_data.append(np.array(indivi_cover_leak_data))
        pop_cover_leak_data = np.array(pop_cover_leak_data)
        for index in range(len(pop_pr)):#单位化如92*10
            indivi_pr=pop_pr[index]
            pop_pr[index]=np.array([single_pr/np.linalg.norm(single_pr) if np.linalg.norm(single_pr)!=0 else single_pr for single_pr in indivi_pr]).T
        pop_project=[]
        for indi_index in range(len(pop_cover_leak_data)):  #作向量内积
            indi_project=np.dot(pop_cover_leak_data[indi_index],pop_pr[indi_index])
            pop_project.append(indi_project)
        # pop_exceed_distance_ratio=[]
        pop_location_performance=[]

        for indi_index in range(len(pop_project)):
            coverLeak_like_index=[np.where(row>self.similarity) for row in pop_project[indi_index]]
            cover_leak=pop_cover[indi_index]
            leak_like_dir=dict(zip(cover_leak,coverLeak_like_index))#相似字典{泄漏节点1：[相似特征节点]，}

            exceed_distance_num=0   #exceed_distance越大代表超出与所有真正泄漏距离阈值的相似泄漏的比例越大
            for leak_node_index in leak_like_dir.keys():
                like_leaks_index=leak_like_dir[leak_node_index][0]
                for like_leak_index in like_leaks_index:
                    if(self.topo_distance[leak_node_index][like_leak_index]>self.distance_threshold):
                        exceed_distance_num = exceed_distance_num + 1
                        break
            pop_location_performance.append(len(cover_leak)-exceed_distance_num)
        return pop_location_performance

    def calCover(self, monitors):
        """
        @param monitors: 监测点对应为染色体/个体
        @param allCoverRelation: 所有节点的覆盖关系
        @return: 个体所覆盖的爆管点
        """
        coverNodes = []
        for nodeIndex in monitors:
            coverNodes.extend(self.allCoverRelation[nodeIndex])
        coverNodes = list(set(coverNodes))
        return coverNodes


# 设置每个节点带有权重的目标函数计算
class doubleMin_withWeight(objectFun_2):
    def __init__(self, population):
        objectFun_2.__init__(self, population)

    # 时间计算
    def objFun_1(self):
      pass

    # 覆盖率计算
    def objFun_2(self,):
        pass

# 测试函数  如下
if __name__ == "__main__":
    from Main.NSGA2.population_init import population
    from Main.tools.disAndNodeDir import distance_nodeDir
    import numpy as np
    from simulation.calCoverRelation import *
    from simulation.readAndDraw import loadSensitiveMat
    prMat=loadSensitiveMat(r"D:\科研\code\sensorLayout\result\Net3\pr.csv")
    allCoverRelation=getCover((r"D:\科研\code\sensorLayout\result\Net3\dFM.csv"))
    p=population(10,10,92)
    inp = "D:/project/Cpp/data/Net3.inp"
    dn=distance_nodeDir(inp)
    topo_distance=dn.topo_distance()
    nodeIndexId=dn.get_nodeIndexId()
    m3 = doubleMax(p, allCoverRelation,prMat,topo_distance,nodeIndexId)
    obj1=m3.objFun_1_Max()
    print(obj1[0])
    m3.objFun_2()
    obj2=m3.objFun_2_Max(obj1[1])
    print(obj2)






