'''
计算各种指数
'''
import datetime
import xlrd
import math
import csv
import os

def getcsv(csvname):
	lines = []
	open_file = open(csvname, 'r',encoding='utf-8')
	csv_reader = csv.reader(open_file)
	for row in csv_reader:
		lines.append(row)
	return lines

def gettxt(filepath):
	f = open(filepath,"r",encoding='utf-8')
	lines = f.readlines() #读取全部内容
	return lines

def save2csv(csvName,list):
	path = './sz50/' + csvName + '.csv'
	if os.path.exists(path):
		os.remove(path)
	print(path)
	csvFile = open(path, 'w',encoding='utf-8',newline='')
	writer = csv.writer(csvFile)
	# writer.writerow(('标题','阅读','评论','字数','影响力','时间'))
	for l in list:
		writer.writerow(l)

def save2txt(fileName,list):
	path = './sz50/' + fileName + '.csv'
	if os.path.exists(path):
		os.remove(path)
	print(path)
	ofile = open(path, 'w',encoding='utf-8')
	for l in list:
		ofile.write(l+"\n")

#上证指数汇总
sz_trades = {}
xlsfile = r'datas/上指数汇总.xlsx' 
data = xlrd.open_workbook(xlsfile)
table = data.sheets()[1]          #通过索引顺序获取
nrows = table.nrows
for i in range(nrows)[2:nrows-1]:
	d = xlrd.xldate.xldate_as_datetime(table.cell(i,0).value,0)	
	dstr = d.strftime('%Y-%m-%d')
	# print(dstr+","+str(table.cell(i,6).value))
	#[今日收盘价,上个交易日收盘价,涨跌幅]
	sz_trades.setdefault(dstr,[table.cell(i,4).value,table.cell(i-1,4).value,table.cell(i,6).value])

#上证银行指数
# sz_bank_trades = {}
# xlsfile = r'datas/上证银行指数.xlsx' 
# data = xlrd.open_workbook(xlsfile)
# table = data.sheets()[0]          #通过索引顺序获取
# nrows = table.nrows
# for i in range(nrows)[1:nrows-2]:
# 	d = xlrd.xldate.xldate_as_datetime(table.cell(i,0).value,0)	
# 	dstr = d.strftime('%Y-%m-%d')
# 	sz_bank_trades.setdefault(dstr,table.cell(i,2).value)

# banks = ["中国银行","工商银行","交通银行","农业银行","浦发银行","招商银行","建设银行"]
xlsfile = r'sz50.xlsx' # 上证50股票名单
data = xlrd.open_workbook(xlsfile)
table = data.sheets()[0]          #通过索引顺序获取
# cols = table.col_values(2)
nrows = table.nrows
banks = []
for i in range(nrows)[1:]:
	banks.append(table.cell(i,0).value)

stock_trades = {}
for bank in banks:
	csvpath = r'datas/trades/'+bank+'.csv' 
	lines = getcsv(csvpath)
	trades = {}	
	i = 1
	for line in lines[2:len(lines)-1]:
		dstr = line[0]
		line.append(lines[i][4])
		trades.setdefault(dstr,line)
		i+=1
	stock_trades.setdefault(bank,trades)

stocks = {}
for bank in banks:
	csvpath = r'datas/'+bank+'.csv' 
	ls = getcsv(csvpath)
	scores = gettxt(r'datas/'+bank+'_socre.txt')
	datas = {}	
	for i in range(len(ls))[1:]:
		l = ls[i]
		# print(l)
		dstr = l[5].split()[0]
		# print(dstr)

		if(dstr not in datas.keys()):
			datas.setdefault(dstr,[])
		lines = datas[dstr]

		line = []
		# print(scores[i-1])
		line.append(scores[i-1])#涨跌
		line.append(l[1])#阅读
		line.append(l[2])#评论
		line.append(l[3])#字数
		line.append(float(l[4]) + 1)#影响力

		lines.append(line)

		datas[dstr] = lines
		stocks.setdefault(bank,datas)

stocks2 = {}
for bank in stocks.keys():
	datas = stocks[bank]
	datas2 = {}

	i = 0
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
			reads += int(line[1])
			comment += int(line[2])
			words_count += int(line[3])

		for line in lines:
			if(int(line[0]) > 0):
				up += 1
				Lt_up += (int(line[1]))/reads * line[4]
			else:
				down += 1
				Lt_down += (int(line[1]))/reads * line[4]

		VOL = 0 #日内波动率
		if(dstr in trades.keys()):
			highest = float(trades[dstr][2])
			lowest = float(trades[dstr][3])
			VOL = math.pow((math.log(highest,math.e) - math.log(lowest,math.e)),2)/(4 * math.log(2,math.e))
		data2.append(VOL)

		#上证日收益率
		if(i > 0):
			if(dstr in sz_trades.keys()):
				endprice = sz_trades[dstr][0]
				lastendprice = sz_trades[dstr][1]
				data2.append(math.log((endprice / lastendprice),math.e))
			else:
				data2.append(0)
		else:
			data2.append(0)

		#日收益率
		if(i > 0):
			if(dstr in trades.keys()):
				endprice = float(trades[dstr][4])
				lastendprice = float(trades[dstr][11])
				data2.append(math.log((endprice / lastendprice),math.e))
			else:
				data2.append(0)
		else:
			data2.append(0)

		SSI = up - down #简单情感指数
		data2.append(SSI)

		BI = math.log((1+up)/(1+down),math.e) #看涨
		data2.append(BI)

		DIS = 1 -  math.sqrt(1 - math.pow((up-down)/(up+down),2)) #意见分散指数
		data2.append(DIS)

		IIAt = math.log((1+Lt_up)/(1+Lt_down),math.e) #影响力指数
		data2.append(IIAt)

		# data2.append(comment/len(lines)) #平均每篇的评论数
		data2.append(comment) #总评论数

		data2.append(words_count/len(lines)) #平均每篇的字数

		data2.append(len(lines)) #发帖量

		trade = 0 #实际涨跌
		if(dstr in trades.keys()):
			trade = trades[dstr][6]
		if(float(trade) > 0): 
			data2.append(1) #涨
		elif(float(trade) < 0):
			data2.append(0) #跌
		else:
			data2.append(2) #不涨不跌

		data2.append(trade)#实际涨跌

		if(dstr in sz_trades.keys()):
			data2.append(sz_trades[dstr][2])#上证指数
		else:
			data2.append(0)

		# if(dstr in sz_bank_trades.keys()):
		# 	data2.append(sz_bank_trades[dstr])#上证银行指数
		# else:
		# 	data2.append(0)

		datas2.setdefault(dstr,data2)
		i += 1

	stocks2.setdefault(bank,datas2)

def exists_date(dstr):
	i = 0
	for bank in stocks2.keys():
		if(dstr not in stocks2[bank].keys()):
			i += 1
	if i > 5:
		return False
	else:
		return True

dates = {}
i = 0
print("日期,日内波动率,上证日收益率,日收益率,简单情感指数,看涨,意见分散指数,影响力指数,总评论数,平均每篇的字数,发帖量,实际涨跌,涨跌幅,上证指数")	
for bank in stocks2.keys():
	# print(bank+"---------------------------------------------------------------------")
	lines = []
	lines.append("日期,日内波动率,上证日收益率,日收益率,简单情感指数,看涨,意见分散指数,影响力指数,总评论数,平均每篇的字数,发帖量,实际涨跌,涨跌幅,上证指数")
	datas = stocks2[bank]
	for dstr in datas.keys():
		# if(not exists_date(dstr)):
		# 	continue
		strs = ''
		for d in datas[dstr]:
			strs+=","+str(d)
		print(dstr+strs)
		lines.append(dstr+strs)
		i+=1
	save2txt(bank+"_dayrate",lines)
print(i)