#!/usr/bin/env python
# encoding: utf-8
import random
'''
@author: 雨夜微凉
@contact: 1475477624@qq.com
@file: mutation.py
@time: 2020/5/23 19:13
@desc:
'''

def mutation(pops,pop_size,chrom_length,pm,nodeIndexList):
    old_chromosome = pops.copy()
    for i in range(pop_size):
        r = random.random()
        n = random.randint(0, chrom_length // 2)  # 在个体的前半段随机选取一个点进行变异
        m = random.randint(chrom_length // 2, chrom_length - 1)  # 在个体的后半段随机选取一个点进行变异
        if r <= pm:
            if pops[i][n] + 1 <= nodeIndexList[-1]:
                pops[i][n] = pops[i][n] + 1  # 整数编码,随机+1或者减1
            if pops[i][m] - 1 >= 0:
                pops[i][m] = pops[i][m] - 1
    for i in range(pop_size):
        length = len(set(pops[i]))
        if length < chrom_length:
            # print(population[i],old_population[i])
            pops[i] = old_chromosome[i]
