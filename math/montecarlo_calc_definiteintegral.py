#Monte Carlo Method for Calculating Definite Integral
 
import math
import random
 
#积分区间
# upper_bound=15
# lower_bound=10
upper_bound=2
lower_bound=1

#========================================================
#导函数
#========================================================
def f_x_(x):
    # outcome=3*(x**2)+4*math.cos(x)-4*x*math.sin(x)
    outcome = 1 / x
    return outcome
 
#========================================================
#原函数
#========================================================
def F_x_(x):
    # outcome=x**3+4*x*math.cos(x)
    outcome = math.log(x)
    return outcome
 
#========================================================
#生成随机数，用蒙特卡洛方法计算定积分
#========================================================
DefiniteIntegral_By_MonteCarloMethod=0
 
#随机生成10000个f(x),10<=x<=15,求和
sum=0
count=1
while count<=10000:
    sum=sum+f_x_(random.uniform(lower_bound,upper_bound))
    count=count+1
 
DefiniteIntegral_By_MonteCarloMethod=(upper_bound-lower_bound)*(sum/10000)
 
print("用蒙特卡洛方法计算的定积分：")
print(DefiniteIntegral_By_MonteCarloMethod)
print("")
 
#========================================================
#直接用原函数求定积分，用于比较结果的偏差程度
#========================================================
DefiniteIntegral_By_PrimitiveFunction=F_x_(upper_bound)-F_x_(lower_bound)
 
print("直接用原函数计算的定积分：")
print(DefiniteIntegral_By_PrimitiveFunction)
print("")
 
#========================================================
#偏差程度
#========================================================
math_deviation=abs(DefiniteIntegral_By_MonteCarloMethod-DefiniteIntegral_By_PrimitiveFunction)/DefiniteIntegral_By_PrimitiveFunction
print("偏差程度为：")
#显示百分比，小数点后保留四位
print('percent: {:.4%}'.format(math_deviation))