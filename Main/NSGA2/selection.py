#!/usr/bin/env python
# encoding: utf-8
'''
@author: 雨夜微凉
@contact: 1475477624@qq.com
@file: selection.py
@time: 2020/6/20 22:43
@desc:
'''
from random import sample, shuffle
from numpy import transpose, vstack


def mycmp2(i, j, fun_score):
    """
    二元锦标赛 方式选择
    :param i:随机个体索引1号
    :param j:随机个体索引2号
    :param fun_score:
    :return:
    """
    s1 = 0
    s2 = 0
    s = fun_score.shape[1]

    for k in range(s):
        if fun_score[i][k] > fun_score[j][k]:
            s1 += 1
        elif fun_score[i][k] < fun_score[j][k]:
            s2 += 1

    if s1 == 0 and s2 != 0:
        return j
    elif s1 != 0 and s2 == 0:
        return i
    else:
        temp = [i, j]
        shuffle(temp)
        return temp[0]


def selection(population, function_object):
    function_object.population = population  # 为函数对象赋值新的种群个体

    # 计算新种群目标函数数值，并建立矩阵 funScore
    obj1=function_object.objFun_1_Max()
    obj2=function_object.objFun_2_Max(obj1[1])
    func_score = vstack((obj1[0], obj2))
    func_score = transpose(func_score)
    # print(funScore)
    N = population.shape[0]
    V = population.shape[1]
    indicate_0 = range(N)
    indicate = []
    for _ in range(N):
        random_index1, random_index2 = sample(indicate_0, 2)
        indicate.append(mycmp2(random_index1, random_index2, func_score))  # 二元锦标赛选择

    population[:] = population[indicate]
    func_score[:] = func_score[indicate]


if __name__ == "__main__":
    # np.random.seed(0)
    # random.seed(0)
    # from function.funUserDefine import *
    # population=np.random.rand(5, 2)
    # functionObject=ZDT1(population)
    # print(population)
    # print(functionObject)
    # selection(population, functionObject)
    # print(population)
    # print(functionObject)
    pass

