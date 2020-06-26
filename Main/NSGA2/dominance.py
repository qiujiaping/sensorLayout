#!/usr/bin/env python
# encoding: utf-8
'''
@author: 雨夜微凉
@contact: 1475477624@qq.com
@file: dominance.py
@time: 2020/6/22 22:19
@desc:
'''
from numpy import arange, array, all

def dominance(funScore):
    """
    支配
    支配关系字典 r_dict
    建立 {个体号码：[支配其的个数， 被其支配的个体列表]}
    :param funScore:
    :return:
    """
    # 支配关系字典
    r_dict = {}
    # 需要建立支配关系的 个体数
    N = funScore.shape[0]
    # 建立个体索引 向量
    indicateVector = arange(N)
    # 建立 元素全为1 的 列向量
    oneVector = array([1] * N).reshape(N, 1)  # 将[1 1 1 1 1 ]改变为[[1]/n[1]/n[1]/n[1]/n[1]]

    for k in range(N):
        # 建立 行向量全为 第k个个体评分的 矩阵
        oneMatrix = oneVector * funScore[k,]  # 生成了全是第k个个体矩阵
        # print("oneMatrix",oneMatrix)
        # 建立支配关系判断的 差分矩阵
        diffMatrix = funScore - oneMatrix  # 原始矩阵减去生成的全是第k个个体的矩阵
        # print("diffMatrix",diffMatrix)
        greaterMatrix = (diffMatrix >= 0)  # 双True则为支配其的个体(越大越好)
        # print(greaterMatrix)
        lessMatrix = (diffMatrix <= 0)  # 双True则为被其支配的个体
        equalMatrix = (diffMatrix == 0)

        # 从行来看，行全为真则该行为真
        greaterVector = all(greaterMatrix, axis=1)
        # print(greaterVector)
        lessVector = all(lessMatrix, axis=1)
        # print(lessVector)
        equalVector = all(equalMatrix, axis=1)

        # 建立非支配、支配向量^两个不一样则取真
        nonDominate= indicateVector[greaterVector ^ equalVector,]
        # print(dominate)
        dominate = indicateVector[lessVector ^ equalVector,]

        # 建立支配关系字典
        r_dict[k] = [len(nonDominate), list(dominate)]#前一个是比我好的，后一个是比我差的

    return r_dict


if __name__ == "__main__":
    funScore = array([[1, 2], [2, 2], [2, 2], [2, 2], [4, 3], [2, 1], [3, 1], [3, 2], [3, 3], [3, 4], [5, 6]])
    # 0      1      2      3     4      5      6       7     8      9      10
    # print(funScore)
    d = dominance(funScore)
    print(d)
    # print(rank(d))
    # p = population(8,2)
    # f=fitness_pop(p)
    # print(f)
    # print(dominance(f))

"""
        支配关系字典 r_dict
        建立 {个体号码：[支配其的个数， 被其支配的个体列表]}
"""

