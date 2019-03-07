#-*- coding:UTF-8 -*-

import math
import stock


years = 10
multiple = 3 # 倍数
currentFlow = 20
profits = 20
growthRate = 0.1 # 未来增长率

r = stock.calcDiscountRate(years,multiple)
print str(years) +"年"+ str(multiple) +"倍贴现率:"+str(r)
stock.calcInterValue(currentFlow,growthRate,r)

# total = stock.calcCashFlow(profits,years,growthRate) + currentFlow
# print "未来"+str(years)+"年内总现金流："+str(total)

# cv = stock.calcCurrentValue(total,years,r)
# print str(years)+"年后的"+str(total)+"贴现，当前值："+str(cv)

# profits = [12.79,18.67,26.86,38.01,49.87,61.68,88.07]

# growthRates = stock.calcGrowthRate(profits)
# for i in range(len(growthRates)):
# 	print "第" + str(i + 2) + "年增长率:"+str(growthRates[i]*100)+"%"

# compoundGrowthRate = stock.calcCompoundGrowthRate(profits)
# print str(len(profits))+"年复合增长率:"+str(compoundGrowthRate*100)+"%"

# avgGrowthRate = stock.calcAvgGrowthRate(profits)
# print str(len(profits))+"年平均增长率:"+str(avgGrowthRate*100)+"%"
