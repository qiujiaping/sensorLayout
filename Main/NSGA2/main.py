#!/usr/bin/env python
# encoding: utf-8
'''
@author: 雨夜微凉
@contact: 1475477624@qq.com
@file: main.py
@time: 2020/6/18 14:49
@desc:
'''
from Main.function.funUserDefine import *
from selection import selection
from crossover import crossover
from mutation import mutation
from dominanceMain import dominanceMain
from Main.NSGA2.population_init import population
import matplotlib.pyplot as plt
from numpy import vstack, array, set_printoptions, transpose
import time
import wntr
class SensorPlacement():
    def __init__(self,inp_path,pr_path,allCoverRelation,pop_size=100, chromosome_len=10,
                 cross_probability=0.8, mutation_probability=0.2, iterations_num=100):
        """
        初始化参数
        :param inp_path: 水力模型位置
        :param pop_size: 种群规模
        :param chromosome_len: 个体数量
        :param cross_probability: 交叉概率
        :param mutation_probability: 变异概率
        :param iterations_num: 迭代次数
        :param nodeIndexId:节点索引ID字典
        """
        self.inp_path=inp_path
        self.pop_size = pop_size
        self.chromosome_len = chromosome_len
        self.cross_probability = cross_probability
        self.mutation_probability = mutation_probability
        self.iterations_num = iterations_num
        self.nodeIndexId=self.getNodeIdIndex()
        self.pr_path=pr_path
        self.allCoverRelation=allCoverRelation


    def getNodeIdIndex(self):
        wn = wntr.network.WaterNetworkModel(self.inp_path)
        nodeID = wn.junction_name_list
        nodeIndexId = {}
        for i in range(len(nodeID)):
            nodeIndexId.update({i: nodeID[i]})
        return nodeIndexId

    def read_csv(self,csv_path,is_normalize=False):
        """
        读取残差矩阵（敏感度矩阵）和泄漏影响矩阵
        当读取残差矩阵文件时需要单位化
        :return:
        """
        with open(csv_path, 'r') as f:
            reader = csv.reader(f)
            Mat = []
            if (is_normalize == True):
                for row in reader:
                    row=list(map(float, row))
                    if(np.linalg.norm(row)==0):
                        Mat.append(row)
                    else:
                        row=row / np.linalg.norm(row)
                        Mat.append(list(map(float, row)))
                Mat = np.array(Mat)
            else:
                for row in reader:
                    Mat.append(list(map(float, row)))
                Mat = np.array(Mat)
        return Mat

    def iteration(self):
        """
        算法迭代主程序
        :return: 最后迭代完成的排序,去重的种群
        """
        node_count=len(self.nodeIndexId.keys())
        pop = population(self.pop_size, self.chromosome_len, node_count)
        prMat=self.read_csv(self.pr_path)
        allCoverRelation=self.allCoverRelation
        func_obj = doubleMin(pop, allCoverRelation,prMat)
        time_start = time.time()
        timelist = []
        for i in range(self.iterations_num):
            copy_pop = pop.copy()
            selection(pop, func_obj)
            crossover(pop, self.cross_probability)
            mutation(pop, self.mutation_probability, node_count-1)
            origin_pop = pop
            temp_pop = vstack((copy_pop, origin_pop))
            func_obj = doubleMin(temp_pop, node_dirt)
            pop = dominanceMain(temp_pop, func_obj)
            print("第 %d 次迭代" % i)
            if(i%10==0):
                timelist.append(time.time()-time_start)
        print(timelist)
        # estimate(pop, func_obj)
        pop_node = array(list(set([tuple(sorted(t)) for t in pop])))      # 个体按数值大小排序, 去重
        return pop_node

    def draw_node(self, pop_result):
        #for i in pop_result:
            #print(i)
        list1 = []
        func_obj = MinMax2(pop_result, self.read_json())
        # estimate(pop_result, func_obj)
        for i in func_obj.objFun_2():
            m = 1-i
            list1.append(m)
        # func_score = np.vstack((func_obj.objFun_1(), func_obj.objFun_2()))
        func_score = vstack((func_obj.objFun_1(), list1))
        print(transpose(func_score))
        # funScore = np.transpose(func_score)
        set_printoptions(suppress=True)
        x = func_score[0]
        y = func_score[1]
        plt.scatter(x, y)
        plt.xlabel("min time")
        plt.ylabel("covered")
        plt.show()


if __name__ == "__main__":
    # 200个个体, 30个变量， 变量数值范围0到2**14
    # 交叉概率0.6， 编译概率0.1
    nodeCount1 = 3628
    jsonFile = "F:\\AWorkSpace\\Python-Learning-Data\\3628node2.json"
    jsonFile4 = "F:\\AWorkSpace\\Python-Learning-Data\\3628node3_weight.json"
    jsonFile2 = "F:\\AWorkSpace\\data\\test\\final_json.json"   # 测试中json中的key和value中的list'内元素都为int
    jsonFile3 = "F:\\AWorkSpace\\Python-Learning-Data\\DDirtnode3.json"
    sp = SensorPlacement(jsonFile4, iterations_num=500)
    node_result = sp.iteration()
    sp.draw_node(node_result)

