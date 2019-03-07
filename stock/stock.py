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

# 计算公司永久价值
def calcInterValue(currentFlow,growthRate,discountRate,years = 10,longGrowthRate=0.03):
	total = 0
	discount = 0
	for i in range(years):
		#先计算前十年每年的现金流 未来现金流 = (1+增长率)^年X初始现金流
		flow = currentFlow * math.pow(1+growthRate,i+1)
		print "未来第"+str(i+1)+"年现金流："+str(flow)
		#再计算这十年的现金流贴现 现金流贴现=未来现金流X【1／(1+贴现率^年数)
		discount = flow * (1/math.pow(1+discountRate,i+1))
		print "未来第"+str(i+1)+"年现金流贴现："+str(flow)
		total = total + discount
	print "未来10年的现金流贴现加总："+str(total)
	#计算并贴现永久价值 永久价值=【第5年或第10年的现金流x(1+预期增长率)】/（贴现率 – 预期增长率）  预期增长率假定为3%
	forever = (discount * (1+longGrowthRate))/(discountRate-longGrowthRate)
	foreverDiscount = forever * (1/math.pow(1+discountRate,years))
	total = total + foreverDiscount
	print "企业总的现值："+str(total)