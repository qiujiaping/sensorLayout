#!/usr/bin/env python
# encoding: utf-8
import random

'''
@author: 雨夜微凉
@contact: 1475477624@qq.com
@file: cross.py
@time: 2020/5/23 19:12
@desc:变异
'''

def cross(pops,pop_size,pc,chrom_length):
    """
    交叉
    @param pops: 种群
    """
    old_chromosome = pops.copy()
    for i in range(pop_size - 1):
        r = random.random()
        if r < pc:
            crossPoint = chrom_length // 2
            for n in range(crossPoint, chrom_length):  # 选择是在个体一半处进行交叉,交换两个个体的后半段
                mid = pops[i][n]
                pops[i][n] = pops[i + 1][n]
                pops[i + 1][n] = mid
    for i in range(pop_size):
        length = len(set(pops[i]))
        if length < chrom_length:
            pops[i] = old_chromosome[i]

