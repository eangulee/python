# 蒙特卡洛求自然对数e
import random
import matplotlib.pyplot as plt
import numpy as np


DARTS = 1024*1024 # 总共撒点的个数
counts = 0 # 落在曲线下方的点数
e = 0 # e的计算值
xs = [0,0]
ys = [0,0]

# 开始画左边的图：撒点估计曲线下方的面积
plt.subplot(121)
x = np.arange(0.5,2.5,0.001)
plt.ylim(0,1.25) # y轴坐标范围
plt.xlabel('x') # x轴标签
plt.ylabel('y') # y轴标签
plt.plot(x,1/x) # 绘制反比例函数曲线
plt.legend(loc=1) # 在右上角增加图例
plt.legend(['y = 1 / x']) # 图例的内容
plt.plot([1,1,2,2],[0,1,1,0],'r',linewidth=0.2) # 绘制撒点范围框

for i in range(DARTS):
    x = random.uniform(1,2)
    y = random.uniform(0,1)
    if y < 1/x: # 点落在曲线下方
        counts += 1
        plt.subplot(121)
        plt.plot(x,y,'g.')
    else: # 点落在曲线上方
        plt.subplot(121)
        plt.plot(x,y,'r.')
    if counts>0:
        e = pow(2,i/counts)

    # 开始画右边的图：e的计算值随投掷次数的关系
    plt.subplot(122)
    xs[0] = xs[1] # 上一个e值与下一个e值，通过xs与ys列表中的两个元素进行两点连线
    xs[1] = i
    ys[0] = ys[1]
    ys[1] = e
    plt.ylim(0,4.5) # y轴坐标范围
    plt.xlabel('Number of try') # x轴标签
    plt.ylabel('Estimation of e') # y轴标签
    plt.yticks(np.arange(0,4.5,0.5)) # y轴刻度线
    plt.title('e:{:.10f}\ncount:{}'.format(e,i)) # 图的标题动态更新
    plt.axhline(np.e,linewidth=0.05,color='r') # 绘制2.71828参考线
    plt.plot(xs,ys,'b--',linewidth=0.3) # 绘制e的计算值随撒点次数变化的曲线
    plt.ion() # 保持图像处于交互更新状态 
    plt.pause(0.001) # 控制撒点速度