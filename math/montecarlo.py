import random
from sympy import *
import numpy as np
import matplotlib.pyplot as plt
import math
#montecarlo 求定积分
def calpai():
    n = 1000000
    r = 1.0
    a, b = (0.0, 0.0)
    x_neg, x_pos = a - r, a + r
    y_neg, y_pos = b - r, b + r

    count = 0
    for i in range(0, n):
        x = random.uniform(x_neg, x_pos)
        y = random.uniform(y_neg, y_pos)
        if x*x + y*y <= 1.0:
            count += 1

    print((count / float(n)) * 4)

#montecarlo 求定积分
def integral():
    n = 10000000
    x_min, x_max = 0.0, 1.0
    y_min, y_max = 0.0, 1.0

    count = 0
    for i in range(0, n):
        x = random.uniform(x_min, x_max)
        y = random.uniform(y_min, y_max)
        # x*x > y，表示该点位于曲线的下面。所求的积分值即为曲线下方的面积与正方形面积的比。
        if x*x > y:
            count += 1

    integral_value = count / float(n)
    print(integral_value)

# 直接求定积分
def integral1():
    x = symbols("x")
    f = x * x
    #integrate(函数，(变量，下限，上限))
    v = integrate(f,(x,0.0,1.0)) 
    print(v)

# integrate ln
def integral_ln():
     a = 1
     b = 2
     x = symbols("x")
     # ln 的导数是 1/x
     f = 1 / x
     v = integrate(f ,(x,1.0,2.0))
     print("integrate:",v)
     print("ln2 - ln1 = ",(math.log(2)))

# montecarlo calc ln
def montecarlo_ln():
    n = 1000000
    x_min, x_max = 1.0, 2.0
    y_min, y_max = 0.0, 1.0

    count = 0
    for i in range(0, n):
        x = random.uniform(x_min, x_max)
        y = random.uniform(y_min, y_max)
        # 1/x > y，表示该点位于曲线的下面。所求的积分值即为曲线下方的面积与正方形面积的比。
        if 1 / x > y:
            count += 1

    integral_value = count / float(n)
    print(integral_value)

if __name__ == '__main__':
    # calpai()
    # integral()
    # integral1()
    integral_ln()
    montecarlo_ln()