#!/usr/bin/env python
# encoding: utf-8
'''
@author: 雨夜微凉
@contact: 1475477624@qq.com
@file: selection.py
@time: 2020/5/23 19:06
@desc:选择
'''
import random

def cumsum(fit_value):
	for i in range(len(fit_value)-2, -1, -1):
		t = 0
		j = 0
		while(j <= i):
			t += fit_value[j]
			j += 1
		fit_value[i] = t
		fit_value[len(fit_value)-1] = 1
	return fit_value





def selection(initPops, fitness):
    """

        《《《《《《《《可能改为锦标赛选择可能更好

    @param initPops: 种群数组
    @param fitness:
    """
    new_fitness = [1 / value for value in fitness.values()]  # 使得越小的越大，方便计算
    total_fitness = sum(new_fitness)
    single_p_list = [value / total_fitness for value in new_fitness]
    temp_sum = 0
    P = []
    P=cumsum(single_p_list)
    # for p in single_p_list:
    #     temp_sum = temp_sum + p
    #     P.append(temp_sum)
    dice = []
    length = len(fitness)
    for i in range(length):  # 预先转好轮盘
        dice.append(random.random())
    dice.sort()
    new_chromosomes = []  # 保存选择的个体的染色体
    # temp_fitness = []  # 保存选择的个体的适应度
    num_in = 0  # 新选择的个体数
    cursor = 0  # 游标，若当前筛子的概率大于游标所指轮盘的概率则游标向前滑动以扩大范围
    keys = list(fitness.keys())
    values = list(fitness.values())
    # 选择
    while num_in < length:
        if (dice[num_in] <= P[cursor]):
            new_chromosomes.append(initPops[keys[cursor]])
            # temp_fitness.append(values[cursor])
            num_in = num_in + 1
        else:
            cursor = cursor + 1
    return new_chromosomes
