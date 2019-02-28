#-*- coding:UTF-8 -*-

import math

# 计算贴现率
def calcDiscountRate(years,multiple):
	# multiple = (1+r)^years
	r = math.pow(multiple, 1.0/years) - 1	
	return r


def calcCurrentValue(money,years,discountRate):
	# currentValue*(1+discountRate)^years = money
	cv = money / math.pow(1+discountRate,years)
	return cv


r = calcDiscountRate(10,5)
print "贴现率:"+str(r)

cv = calcCurrentValue(100,10,0.15)
print "十年后的100贴现，当前值："+str(cv)