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
	open_file = open(csvname, 'r',encoding='utf-8')
	csv_reader = csv.reader(open_file)
	for row in csv_reader:
		lines.append(row)
	return lines

def getstocks():
	xlsfile = r'sz50.xlsx' # 上证50股票名单
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
# print(startdate.strftime('%x'))
xlsfile = r'上指数汇总.xlsx' # 上证指数数据
data = xlrd.open_workbook(xlsfile)
table = data.sheets()[1]          #通过索引顺序获取
nrows = table.nrows
sz_datas = {} # 上证收盘数据
for i in range(nrows)[1:]:	
	d = xlrd.xldate.xldate_as_datetime(table.cell(i,0).value,0)
	if(d >= startdate):
		dstr = d.strftime('%x')
		# print(dstr+":"+str(table.cell(i,4).value))
		sz_datas.setdefault(dstr,table.cell(i,4).value)

stocks = getstocks()
stock_datas = {}	# 股票收盘数据
for k in stocks.keys():
	stock_data = {}
	lines = getcsv(r"./stock_spider/dataWithName/{}.csv".format(k))
	for line in lines[1:]:		
		d = datetime.datetime.strptime(line[0], "%Y-%m-%d")
		dstr = d.strftime('%x')
		# print(dstr+":"+str(line[4]))
		stock_data.setdefault(dstr,line[4])	
	stock_datas.setdefault(k,stock_data)

emotion_datas = {} # 情感得分
for k in stocks.keys():
	# print(k+":"+str(stocks[k]))
	emotion_data = {}
	try:
		lines = getcsv(r"sz50/{}.csv".format(k))
		emotions = {}
		for line in lines[1:]:
			length = len(line)
			# try:
			d = datetime.datetime.strptime(line[length-2].split()[0], "%Y-%m-%d")
			dstr = d.strftime('%x')
			# print(dstr+":"+str(line[length-1]))
			# stock_data.setdefault(dstr,line[4])
			if(dstr not in emotions.keys()):
				emotions.setdefault(dstr,[])
			emotionlist = emotions[dstr]
			emotion = float(line[length-1])
			if(emotion >= 0.6):
				emotionlist.append(1)
			elif (emotion <= 0.3):
				emotionlist.append(-1)
			else:
				emotionlist.append(0)
			# print(str(emotion)+","+str(len(emotionlist)))
			emotions.setdefault(dstr,emotionlist)
			# except:
			# 	continue
		for t in emotions.keys():
			emotionlist = emotions[t]
			average_emotion = 0
			for emotion in emotionlist:
				average_emotion += emotion
			# print(k+","+t+","+str(average_emotion))
			emotion_data.setdefault(t,average_emotion)
		emotion_datas.setdefault(k,emotion_data)
	except:
		continue

print('--------------------------------------------------------------------')
print("股票,日期,收盘价,上证指数,简单情感指数")
for k in stock_datas.keys():
	stock_data = stock_datas[k]
	for d in stock_data.keys():
		try:
			emotion_data = emotion_datas[k]
			emotion = 0
			if(d in emotion_data.keys()):
				emotion = emotion_data[d]
			print(k+","+d+","+str(stock_data[d])+","+str(sz_datas[d])+","+str(emotion))			
		except:
			continue





