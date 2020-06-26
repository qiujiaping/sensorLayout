#!/usr/bin/env python
# encoding: utf-8
'''
@author: 雨夜微凉
@contact: 1475477624@qq.com
@file: test.py
@time: 2020/6/13 9:36
@desc:测试残差向量和敏感度矩阵投影（做了实验灵敏度与泄漏量无关）
'''
from simulation import readAndDraw
import numpy as np

def cut(num, c):
    str_num = str(num)
    return float(str_num[:str_num.index('.') + 1 + c])
def projection(SensitiveFileName,pressureResidualMatName):
    unitMat=readAndDraw.loadSensitiveMat(SensitiveFileName)
    unitMat=unitMat.T
    column=len(unitMat[0])
    pressureResidualMat=readAndDraw.loadPressureResidualMat(pressureResidualMatName)
    row=len(pressureResidualMat)
    project=np.zeros(shape=(row,column))
    sensors=[10,26,40,50,58,60,70]
    for i in range(row):
        temp1=[]
        pr=pressureResidualMat[i]
        for k in range(len(sensors)):
            temp1.append(pr[sensors[k]])
        unitTemp1=temp1 / np.linalg.norm(temp1)
        for j in range(column):
            temp2=[]
            unitTemp2=unitMat[:,j]
            for w in range(len(sensors)):
                temp2.append(unitTemp2[sensors[w]])
            unitTemp2= temp2 / np.linalg.norm(temp2)
            dotProduct = unitTemp1.dot(unitTemp2)
            project[i][j]=cut(dotProduct,1)
    return project


if __name__=="__main__":
    sensitiveFile=r"D:/科研/code/sensorLayout/result/Net3sensitive.csv"
    pressureResidualMatFile=r"D:/科研/code/sensorLayout/result/Net3pressureResidualMat.csv"
    projection(sensitiveFile,pressureResidualMatFile)