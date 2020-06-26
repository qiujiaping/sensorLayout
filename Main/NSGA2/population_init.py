#!/usr/bin/env python
# encoding: utf-8
'''
@author: 雨夜微凉
@contact: 1475477624@qq.com
@file: population_init.py
@time: 2020/6/18 15:50
@desc:
'''
from numpy import array
from random import sample

def population(p_num,chromosome_len,node_num):
    """
    生成种群
    :param p_num:  种群规模
    :param i_num:  染色体长度
    :param node_num:  节点数量[管网节点总数]
    :return: population_list
    """
    nodeIndexList = list(range(node_num))
    population_list=[]
    for p in range(p_num):
        i_list = sorted(sample(nodeIndexList,chromosome_len))  # 从list中拿不重复个数的list
        population_list.append(i_list)  # 根据种群规模加入到大的list中
    population_list = array(population_list)   # 将初始的list改为np的list
    # population_list=np.sort(population_list)    # 排序
    return population_list


if __name__ == "__main__":
    p = population(100,10,92)
    print(p)
    #p = createList(100)
    #print(p)


