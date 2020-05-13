import numpy as np
from fractions import Fraction
def get_comparisonMatrix(filePath):
    fr = open(filePath)
    data = fr.readlines()
    column = len(data[0].strip().split(','))
    row = len(data)
    index = 0
    judgeMatrix = np.zeros((row,column))
    for line in data:
        item = line.strip().split(',')
        newList = []
        for i in range(len(item)):
            value = Fraction(item[i])+0.0
            newList.append(value)
        judgeMatrix[index,:] = newList[0:column]
        index += 1
    return judgeMatrix
def ahp(filePath):
    """
    由公式推导得到的权重
    @param data: 比较矩阵
    @return: 标准权重
    """
    data=get_comparisonMatrix(filePath)
    b = []
    cb=9
    for row in data:
        b.append(sum(row))
    B=max(b)-min(b)

    C=[] #C为判断矩阵，根据公式求得
    for row in range(len(data)):
        temp=[]
        for column in range(len(data[0])):
            temp.append(np.power(cb,(b[row]-b[column])/B))
        C.append(temp)

    #存放判断矩阵的每行累乘值，准备用于求权
    M=[]
    for row in range(len(C)):
        temp=1
        for column in range(len(C[0])):
            temp=temp*C[row][column]
        M.append(temp)

    #获得未标准化的权
    weigth=[]
    for v in M:
        weigth.append(np.power(v,1/len(M)))
    # 获得标准化的权
    standWeight=[]
    weigth_sum=np.sum(weigth)
    for v in weigth:
        standWeight.append(v/weigth_sum)

    #开始检查一致性
    D=np.dot(C,standWeight)
    maxRoot=0
    for i in range(len(b)):
        maxRoot=maxRoot+D[i]/(4*standWeight[i])
    consistent=(maxRoot-len(standWeight))/(len(standWeight)-1)
    if(consistent<0.1):
        print("通过一致性检查")
    else:
        print("一致性检查没通过")
    standWeight=np.array(standWeight)
    return standWeight

if __name__=="__main__":

    filePath = u'data/data.txt'
    comparisonMatrix=get_comparisonMatrix(filePath)
    ahp(comparisonMatrix)