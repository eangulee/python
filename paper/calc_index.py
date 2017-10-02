'''
计算各种指数
'''
import datetime
import xlrd
import math

#上证指数汇总
sz_trades = {}
xlsfile = r'datas/上指数汇总.xlsx' 
data = xlrd.open_workbook(xlsfile)
table = data.sheets()[1]          #通过索引顺序获取
nrows = table.nrows
for i in range(nrows)[1:]:
	d = xlrd.xldate.xldate_as_datetime(table.cell(i,0).value,0)	
	dstr = d.strftime('%Y-%m-%d')
	# print(dstr+","+str(table.cell(i,6).value))
	sz_trades.setdefault(dstr,table.cell(i,6).value)

#上证银行指数
sz_bank_trades = {}
xlsfile = r'datas/上证银行指数.xlsx' 
data = xlrd.open_workbook(xlsfile)
table = data.sheets()[0]          #通过索引顺序获取
nrows = table.nrows
for i in range(nrows)[1:]:
	d = xlrd.xldate.xldate_as_datetime(table.cell(i,0).value,0)	
	dstr = d.strftime('%Y-%m-%d')
	sz_bank_trades.setdefault(dstr,table.cell(i,2).value)

banks = ["中国银行","工商银行","交通银行","农业银行","浦发银行","招商银行","建设银行"]

stock_trades = {}
for bank in banks:
	xlsfile = r'datas/'+bank+'股票.xlsx' 
	data = xlrd.open_workbook(xlsfile)
	table = data.sheets()[0]          #通过索引顺序获取
	# cols = table.col_values(2)
	nrows = table.nrows
	trades = {}	
	for i in range(nrows)[1:]:
		# stock = str(table.cell(i,1).value)
		d = xlrd.xldate.xldate_as_datetime(table.cell(i,0).value,0)	
		dstr = d.strftime('%Y-%m-%d')
		trades.setdefault(dstr,table.cell(i,1).value)
	stock_trades.setdefault(bank,trades)

stocks = {}
for bank in banks:
	xlsfile = r'datas/'+bank+'.xlsx' 
	data = xlrd.open_workbook(xlsfile)
	table = data.sheets()[0]          #通过索引顺序获取
	# cols = table.col_values(2)
	nrows = table.nrows
	datas = {}	
	for i in range(nrows)[1:]:
		# stock = str(table.cell(i,1).value)
		d = xlrd.xldate.xldate_as_datetime(table.cell(i,6).value,0)	
		dstr = d.strftime('%Y-%m-%d')
		# print(dstr)

		if(dstr not in datas.keys()):
			datas.setdefault(dstr,[])
		lines = datas[dstr]

		line = []
		line.append(table.cell(i,1).value)#涨跌
		line.append(table.cell(i,2).value)#阅读
		line.append(table.cell(i,3).value)#评论
		line.append(table.cell(i,4).value)#字数
		line.append(table.cell(i,5).value + 1)#影响力

		lines.append(line)

		datas[dstr] = lines
		stocks.setdefault(bank,datas)

stocks2 = {}
for bank in stocks.keys():
	datas = stocks[bank]
	datas2 = {}

	trades = stock_trades[bank] # 交易数据
	for dstr in datas.keys():
		data2 = []

		lines = datas[dstr]
		up = 0 #涨
		down = 0 #跌

		Lt_up = 0 #用于计算影响力指数
		Lt_down = 0

		reads = 0 #总阅读量
		comment = 0 #评论数
		words_count = 0 #字数
		for line in lines:
			reads += line[1]
			comment += line[2]
			words_count += line[3]

		for line in lines:
			if(line[0] > 0):
				up += 1
				Lt_up += (line[1])/reads * line[4]
			else:
				down += 1
				Lt_down += (line[1])/reads * line[4]

		SSI = up - down #简单情感指数
		data2.append(SSI)

		BI = math.log((1+up)/(1+down),math.e) #看涨
		data2.append(BI)

		DIS = 1 -  math.sqrt(1 - math.pow((up-down)/(up+down),2)) #意见分散指数
		data2.append(DIS)

		IIAt = math.log((1+Lt_up)/(1+Lt_down),math.e) #影响力指数
		data2.append(DIS)

		data2.append(comment/len(lines)) #平均每篇的评论数

		data2.append(words_count/len(lines)) #平均每篇的字数

		data2.append(len(lines)) #发帖量

		trade = 0 #实际涨跌
		if(dstr in trades.keys()):
			trade = trades[dstr]
		if(trade > 0): 
			data2.append(1) #涨
		elif(trade < 0):
			data2.append(0) #跌
		else:
			data2.append(2) #不涨不跌

		data2.append(trade)#实际涨跌

		if(dstr in sz_trades.keys()):
			data2.append(sz_trades[dstr])#上证指数
		else:
			data2.append(0)

		if(dstr in sz_bank_trades.keys()):
			data2.append(sz_bank_trades[dstr])#上证银行指数
		else:
			data2.append(0)

		datas2.setdefault(dstr,data2)

	stocks2.setdefault(bank,datas2)

def exists_date(dstr):
	for bank in stocks2.keys():
		if(dstr not in stocks2[bank].keys()):
			return False
	return True

dates = {}
for bank in stocks2.keys():
	print(bank+"---------------------------------------------------------------------")
	print("日期,简单情感指数,看涨,意见分散指数,影响力指数,平均每篇的评论数,平均每篇的字数,发帖量,实际涨跌,涨跌幅,上证指数,上证银行指数")
	datas = stocks2[bank]
	for dstr in datas.keys():
		# if(not exists_date(dstr)):
		# 	continue
		strs = ''
		for d in datas[dstr]:
			strs+=","+str(d)
		print(dstr+strs)