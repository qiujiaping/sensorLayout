import os
import wntr
import numpy as np
import matplotlib.pyplot as plt
import csv
from mpl_toolkits.mplot3d import Axes3D
"""
该模块是获得敏感度矩阵和将来获取需求影响矩阵，并保存数据到文件
1GPM=0.063L/s
1L/s=15.85GPM
"""
class Data:
    def __init__(self,exePath:str,writeFile:str,inp:str,rpt:str,leakFlow:float):
        self.exePath=exePath
        self.writeFile=writeFile
        self.inp=inp
        self.rpt = rpt
        wn = wntr.network.WaterNetworkModel(self.inp)
        self.wn = wn
        print(wn.options.hydraulic.en2_units)
        if(wn.options.hydraulic.en2_units=='GPM'):
            self.leakFlow=leakFlow/0.063 #输入考虑L/S，如果inp文件是GPM，实例初始化转换为GPM
        else:
            self.leakFlow = leakFlow    #输入考虑L/S，实例初始化转换为GPM
        self.pressureAllNodeLeak=None  #泄漏压力矩阵，列节点压力，行泄漏节点，对应于0h，util不定
        self.pressure_at_0hr=None #正常压力向量0h，单位强制转为PSI
        self.SensitiveMat=None
        self.__pressureResidual=None
        self.demandFluMat=None



    def __simLeakSingle(self,leakNodeIndex:int)-> None:
        """
        调用epanet生成数据
        """
        callParam = self.exePath + " " + self.writeFile + " " + self.inp + " " + self.rpt + " " + str(self.leakFlow) + " " + str(leakNodeIndex)
        os.system(callParam)
        # 移除自动生成的rpt文件
        os.remove(self.rpt)


    def __simLeakAll(self):
        """
        模拟所有节点泄漏并获得0时刻的压力数据
        """
        wn = wntr.network.WaterNetworkModel(self.inp)
        pressureAllNodeLeak=[]
        for i in range(len(wn.junction_name_list)): #下一步这里要改变（只让筛选的节点泄漏模拟）
            leakNodeIndex=i+1
            # 逐个节点模拟，需及时压力写入的文件处理文件
            self.__simLeakSingle(leakNodeIndex)
            pressureAllNodeLeak.append(self.__readPressureLeak())
        self.pressureAllNodeLeak=np.array(pressureAllNodeLeak)

    def __readPressureLeak(self)->np.ndarray:
        """
        返回0时刻的值，np.ndarray类型数据，单位不一定（取决于inp文件的单位，这和EPANET的机制有关）
        """
        with open(self.writeFile) as f:
            row=0
            pressureAllTime=[]
            for line in f.readlines():
                if(row==0):
                    row = row + 1
                    continue
                pressureAllTime.append(list(map(float,line.split()[1:])))
                row = row + 1
            # 压制科学计数法
            np.set_printoptions(suppress=True)

            #泄漏完整延时压力数据
            pressureAllTime=np.array(pressureAllTime)
        # print(pressureAllTime[0])
        return pressureAllTime[0]


    def __simulationNormal(self)->np.ndarray:
        """
        进行正常工况模拟，返回0时的节点压力，单位强制同EPANET保持一致(不转wntr会统一转为si)
        """
        wn = wntr.network.WaterNetworkModel(self.inp)
        sim = wntr.sim.EpanetSimulator(wn)
        result = sim.run_sim()
        pressure_at_0hr = result.node["pressure"].loc[0, :]
        np.set_printoptions(suppress=True)
        if(wn.options.hydraulic.en2_units=='GPM'):
            # 把公制单位转换为美制（计算的值）
            pressure_at_0hr=wntr.epanet.util.from_si(wntr.epanet.util.FlowUnits.GPM,pressure_at_0hr,wntr.epanet.util.HydParam.Pressure )
        # 移除自动生成的rpt文件
        os.remove("temp.bin")
        os.remove("temp.inp")
        os.remove("temp.rpt")
        # 压制科学计数法
        np.set_printoptions(suppress=True)
        self.pressure_at_0hr=np.array(pressure_at_0hr)
        # print(list(pressure_at_0hr))
        return self.pressure_at_0hr


    def __getPressureResidual(self):
        """
        得到压力残差
        """
        # 压制科学计数法
        np.set_printoptions(suppress=True)
        self.__pressureResidual=-(self.pressureAllNodeLeak-self.pressure_at_0hr)
        return self.__pressureResidual


    def __getSensitiveMat(self):
        """
        1:同时调用泄漏全部和正常，得到压差和敏感度矩阵
        2:规范化，单位化

        """
        self.__simLeakAll()
        self.__simulationNormal()
        self.__getPressureResidual()
        # 压制科学计数法
        np.set_printoptions(suppress=True)
        SensitiveMat=self.__pressureResidual/self.leakFlow
        self.SensitiveMat=SensitiveMat

    def saveSensitiveMat(self):
        """
        resultPath为文件生成目录（文件夹）
        """
        self.__getSensitiveMat()
        origiName = os.path.split(os.path.realpath(self.rpt))[1].split(".")[0]
        SensitiveFileName="D:/科研/code/sensorLayout/result/%ssensitive.csv"%origiName
        np.savetxt(SensitiveFileName, self.SensitiveMat, delimiter=',')
    # def loadSensitiveMat(self,SensitiveFileName):
    #     """
    #     从生成的结果文件当中获得原始敏感矩阵
    #     且对敏感矩阵->规范化->单位化
    #     """
    #     with open(SensitiveFileName, 'r') as f:
    #         reader = csv.reader(f)
    #         sensitiveMat=[]
    #         for row in reader:
    #             sensitiveMat.append(list(map(float,row)))
    #     sensitiveMat=np.array(sensitiveMat)
    #     # 规范化
    #     nomarMat = np.array([row / np.max(row) for row in sensitiveMat])
    #     # 单位化
    #     unitMat=np.array([row/np.linalg.norm(row) for row in nomarMat])
    #     return unitMat
    def saveDemandFMAndPressRe(self):
        """
            得到泄漏影响矩阵
        """
        self.__getSensitiveMat()
        # 原始的泄漏影响矩阵
        pressureChangeValue = np.zeros(shape=(len(self.pressureAllNodeLeak), len(self.pressureAllNodeLeak[0])))
        for i in range(len(self.pressureAllNodeLeak)):
            for j in range(len(self.pressureAllNodeLeak[i])):
                if (self.pressureAllNodeLeak[i][i] - self.pressure_at_0hr[i] != 0):
                    pressureChangeValue[i][j] = (abs(self.pressureAllNodeLeak[i][j] - self.pressure_at_0hr[j]))/(abs(self.pressureAllNodeLeak[i][i] - self.pressure_at_0hr[i]))
        self.demandFluMat= np.zeros(shape=(len(self.pressureAllNodeLeak), len(self.pressureAllNodeLeak[0])))

        #标准化
        for i in range(len(self.pressureAllNodeLeak)):
            maxValue=np.max(pressureChangeValue[i])
            minValue=np.min(pressureChangeValue[i])

            for j in range(len(self.pressureAllNodeLeak[i])):
                if ( maxValue-minValue!= 0):
                    self.demandFluMat[i][j] = (pressureChangeValue[i][j] - minValue)/(maxValue-minValue)
        origiName = os.path.split(os.path.realpath(self.rpt))[1].split(".")[0]
        SensitiveFileName = "D:/科研/code/sensorLayout/result/%sdemandFluMat.csv" % origiName
        np.savetxt(SensitiveFileName, self.demandFluMat, delimiter=',')

        # 保存压力残差矩阵
        pressureResidualName = "D:/科研/code/sensorLayout/result/%spressureResidualMat.csv" % origiName
        np.savetxt(pressureResidualName, self.__pressureResidual, delimiter=',')




    # def drawSenPic(self):
    #     """
    #       以三维的形式画出敏感度矩阵
    #     """
    #     plt.rcParams['font.sans-serif'] = ['SimHei']
    #     plt.rcParams['axes.unicode_minus'] = False
    #
    #     unitMat=self.loadSensitiveMat("D:/科研/code/sensorLayout/result/Net3SM.csv")
    #     r,c=unitMat.shape  #r代表泄漏节点数，c代表节点数
    #     # 构造需要显示的值
    #     X = np.arange(0, c, step=1)  # X轴的坐标
    #     Y = np.arange(0, r, step=1)  # Y轴的坐标
    #     # 设置每一个（X，Y）坐标所对应的Z轴的值
    #     Z = unitMat
    #     xx, yy = np.meshgrid(X, Y)  # 网格化坐标
    #     X, Y = xx.ravel(), yy.ravel()  # 矩阵扁平化
    #     bottom = np.zeros_like(X)  # 设置柱状图的底端位值
    #     Z = Z.ravel()  # 扁平化矩阵
    #     width = height = 1  # 每一个柱子的长和宽
    #     # 绘图设置
    #     fig = plt.figure()
    #     ax = fig.gca(projection='3d')  # 三维坐标轴
    #     ax.bar3d(X, Y, bottom, width, height, Z)  #
    #     # 坐标轴设置
    #     ax.set_xlabel('X(节点)')
    #     ax.set_ylabel('Y（泄漏节点）')
    #     ax.set_zlabel('Z(敏感度(value))')
    #     plt.show()
if __name__=="__main__":
    exePath = "D:/project/Cpp/EpanetSimulation/Debug/EpanetSimulation.exe"
    writePFN = "D:/project/Cpp/result/Net3pressure.txt"
    inp = "D:/project/Cpp/data/Net3.INP"
    rpt = "D:/project/Cpp/result/Net3.rpt"
    #生成敏感度是总需水量的2%--16.6L/s，残差向量是3%--24.8L/s
    leakFlow = 24.8   #L/s
    # leakNodeIndex = 10
    data=Data(exePath,writePFN,inp,rpt,leakFlow)
    data.saveSensitiveMat()
    data.saveDemandFMAndPressRe()













