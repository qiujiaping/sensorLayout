import numpy as np
import matplotlib.pyplot as plt
import csv
from mpl_toolkits.mplot3d import Axes3D
from simulation.Mat import Data

def loadSensitiveMat(SensitiveFileName)-> object:
    """
    从生成的结果文件当中获得原始敏感矩阵
    且对敏感矩阵->规范化->单位化
    """
    with open(SensitiveFileName, 'r') as f:
        reader = csv.reader(f)
        sensitiveMat = []
        for row in reader:
            sensitiveMat.append(list(map(float, row)))
    sensitiveMat = np.array(sensitiveMat)
    # 单位化
    unitMat = np.array([row / np.linalg.norm(row) for row in sensitiveMat])
    return unitMat


def loadDemandFluMat(DemandFluMatName)->np.ndarray:

    """
    从生成的结果文件当中获得标准的泄漏影响矩阵
    且对敏感矩阵->规范化->单位化
    """
    with open(DemandFluMatName, 'r') as f:
        reader = csv.reader(f)
        DemandFluMat = []
        for row in reader:
            DemandFluMat.append(list(map(float, row)))
    DemandFluMat = np.array(DemandFluMat)
    return DemandFluMat

def loadPressureResidualMat(pressureResidualMatName)->np.ndarray:

    """
    从生成的结果文件当中获得标准的泄漏影响矩阵
    且对敏感矩阵->规范化->单位化
    """
    with open(pressureResidualMatName, 'r') as f:
        reader = csv.reader(f)
        pressureResidualMat = []
        for row in reader:
            pressureResidualMat.append(list(map(float, row)))
    pressureResidualMat = np.array(pressureResidualMat)
    return pressureResidualMat

def drawSenPic(data):
    """
      以三维的形式画出敏感度矩阵
    """
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    r, c = data.shape  # r代表泄漏节点数，c代表节点数
    # 构造需要显示的值
    X = np.arange(0, c, step=1)  # X轴的坐标
    Y = np.arange(0, r, step=1)  # Y轴的坐标
    # 设置每一个（X，Y）坐标所对应的Z轴的值
    Z = data
    xx, yy = np.meshgrid(X, Y)  # 网格化坐标
    X, Y = xx.ravel(), yy.ravel()  # 矩阵扁平化
    bottom = np.zeros_like(X)  # 设置柱状图的底端位值
    Z = Z.ravel()  # 扁平化矩阵
    width = height = 1  # 每一个柱子的长和宽
    # 绘图设置
    fig = plt.figure()
    ax = fig.gca(projection='3d')  # 三维坐标轴
    ax.bar3d(X, Y, bottom, width, height, Z)  #
    # 坐标轴设置
    ax.set_xlabel('X(节点)')
    ax.set_ylabel('Y（泄漏节点）')
    ax.set_zlabel('Z(敏感度(value))')
    plt.show()


if __name__=="__main__":
    # exePath = "D:/project/Cpp/EpanetSimulation/Debug/EpanetSimulation.exe"
    # writePFN = "D:/project/Cpp/result/pressure.txt"
    # inp = "D:/project/Cpp/data/Net3.inp"
    # rpt = "D:/project/Cpp/result/Net3.rpt"
    # leakFlow = 6.3
    # leakNodeIndex = 10
    # data = Data(exePath, writePFN, inp, rpt, leakFlow)
    # data.saveSensitiveMat()
    mat=loadSensitiveMat("D:/科研/code/sensorLayout/result/ky8.csv")
    # drawSenPic(mat)
