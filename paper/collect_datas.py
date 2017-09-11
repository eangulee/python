import xlrd
import datetime
import csv

def dict2list(dic:dict):
    ''' 将字典转化为列表 '''
    keys = dic.keys()
    vals = dic.values()
    lst = [(key, val) for key, val in zip(keys, vals)]
    return lst

def getcsv(csvname):
	lines = []
	csv_reader = csv.reader(open(csvname, encoding='utf-8'))
	for row in csv_reader:
		lines.append(row)
	return lines

def getstocks():
	xlsfile = r'D:\python\paper\sz50.xlsx' # 上证50股票名单
	data = xlrd.open_workbook(xlsfile)
	table = data.sheets()[0]          #通过索引顺序获取
	nrows = table.nrows
	stocks = {}
	for i in range(nrows)[1:]:
		stockname = table.cell(i,0).value
		stock = str(table.cell(i,1).value)
		stock = stock.replace('.0','')
		if(len(stock) < 6):# 股票代码为6位
			diff = 6 - len(stock)
			for j in range(diff):
				stock = '0' + stock
		# print(stock)
		stocks.setdefault(stockname,stock)
	return stocks

startdate = datetime.datetime.strptime("2015-09-01", "%Y-%m-%d")
print(startdate.strftime('%x'))
xlsfile = r'D:\python\python\paper\上指数汇总.xlsx' # 上证指数数据
data = xlrd.open_workbook(xlsfile)
table = data.sheets()[1]          #通过索引顺序获取
nrows = table.nrows
sz_datas = {} # 上证收盘数据
for i in range(nrows)[1:]:	
	d = xlrd.xldate.xldate_as_datetime(table.cell(i,0).value,0)
	if(d >= startdate):
		dstr = d.strftime('%x')
		sz_datas.setdefault(dstr,table.cell(i,4).value)
		# print(dstr+":"+str(dates[dstr]))

stocks = getstocks()
stock_datas = {}	# 股票收盘数据
for k in stocks.keys():
	# print(k+":"+str(stocks[k]))
	stock_data = {}
	lines = getcsv(r"D:\python\python\paper\stock_spider\dataWithName\{}.csv".format(k))
	for line in lines[1:]:		
		d = datetime.datetime.strptime(line[0], "%Y-%m-%d")
		dstr = d.strftime('%x')
		# print(dstr+":"+str(line[4]))
		stock_data.setdefault(dstr,line[4])	

emotion_datas = {} # 情感得分
for k in stocks.keys():
	# print(k+":"+str(stocks[k]))
	stock_data = {}
	lines = getcsv(r"D:\python\python\paper\sz50\{}.csv".format(k))
	for line in lines[1:]:
		try:
			d = datetime.datetime.strptime(line[3].split()[0], "%Y-%m-%d")
			dstr = d.strftime('%x')
			print(dstr+":"+str(line[4]))
			# stock_data.setdefault(dstr,line[4])
		except:
			continue