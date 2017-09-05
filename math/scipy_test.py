# reference:https://uqer.io/community/share/54d83bb3f9f06c276f651a6e

import numpy as np
import scipy.stats as stats
import scipy.optimize as opt

'''
# 生成随机数
# 生成n个随机数可用rv_continuous.rvs(size=n)或rv_discrete.rvs(size=n)，
# 其中rv_continuous表示连续型的随机分布，如均匀分布（uniform）、正态分布（norm）、贝塔分布（beta）等；
# rv_discrete表示离散型的随机分布，如伯努利分布（bernoulli）、几何分布（geom）、泊松分布（poisson）等。
# 生成10个[0, 1]区间上的随机数和10个服从参数a=4，b=2的贝塔分布随机数：
rv_unif = stats.uniform.rvs(size=10)
print(rv_unif)
rv_beta = stats.beta.rvs(size=10, a=4, b=2)
print(rv_beta)
'''

# 假设检验
# 生成一组数据，并查看相关的统计量

norm_dist = stats.norm(loc=0.5, scale=2)
n = 200
dat = norm_dist.rvs(size=n)
print("mean of data is: " + str(np.mean(dat)))
print("median of data is: " + str(np.median(dat)))
print("standard deviation of data is: " + str(np.std(dat)))