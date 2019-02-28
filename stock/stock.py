#-*- coding:UTF-8 -*-

import math

# 计算贴现率
def calcDiscountRate(years,multiple):
	# multiple = (1+r)^years
	r = math.pow(multiple, 1.0/years) - 1	
	return r

# 计算现金流贴现
def calcCurrentValue(money,years,discountRate):
	# currentValue*(1+discountRate)^years = money
	cv = money / math.pow(1+discountRate,years)
	return cv

# 计算总现金流
def calcCashFlow(currentValue,years,growthRate):
	total = 0
	for i in range(years):		
		v = math.pow(1 + growthRate,i+1) * currentValue
		total += v
	return total

# 计算增长率
def calcGrowthRate(profits):
	i = 0
	growthRates = []
	for p in profits[1:]:
		# print str(p) +" - " + str(profits[i]) +" / " + str(abs(profits[i]))
		g = (p - profits[i]) / abs(profits[i])		
		growthRates.append(g)
		i += 1

	return growthRates

# 计算复合增长率
def calcCompoundGrowthRate(profits):
	growthRates = calcGrowthRate(profits)
	total = growthRates[0] + 1
	for g in growthRates[1:]:
		total *= (g + 1)
	years = len(profits)
	# 总增长率 = (1+复合增长率)^年数
	compound = math.pow(total,1.0/years)-1.0

	# print str(total)+","+str(1.0/years)+" "+ str(math.pow(total,1.0/years))
	# print compound
	return compound

# 计算平均增长率
def calcAvgGrowthRate(profits):
	growthRates = calcGrowthRate(profits)
	total = growthRates[0]
	for g in growthRates[1:]:
		total += g 
	years = len(profits)
	# 总增长率 = (1+平均增长率)*年数
	avg = (total / years)

	return avg