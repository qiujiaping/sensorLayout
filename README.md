## **布局代码**
_1：读取文件获得压力数据_

_2：构造泄漏特征矩阵_（泄漏定位）

    2.1：正常模拟
    2.2：异常模拟
    2.3：构造矩阵（规范化）
    2.4：图形直观显示

_3：构造节点影响矩阵_（泄漏覆盖/发现）
    
    2.1：正常模拟
    2.2：异常模拟
    2.3：构造矩阵（规范化）
_4：目标函数/评价准则确定_
    
    遗传算法的确定（NSGA）
    
`运用：1:先运行模拟模块的Mat.py选择水力模型等参数得到灵敏度矩阵（水力模型文件名.csv）保存在本项目的结果文件夹里
      2:再运行Main模块的main文件来求解`
      
泄漏规模与泄漏与特征无关，所以可以直接利用敏感度矩阵而不用残差向量除非考虑不确定性

目前有几条路：
1：泄漏定位：高于0.9且距离在一个阈值范围内算定位成功（考虑鲁棒性；平均25小时的敏感度来计算投影）
2：考虑不确定性
    利用蒙特卡洛模拟抽样获得压力的方差分别取不同的权重作为惩罚，权重大，则传感器会远离不确定性大的地方为了定位的效益（适应度函数），权重小，
即不怎么考虑波动性则传感器会在区域分散
3：考虑多目标
4：膨胀集
5：实验环节
    1）通过泄漏定位方法分为高概率区，低概率区，实际泄漏位置，预测位置
    2）混淆矩阵
    3）评价指标：ATD，AC