import xlrd
import csv
import time,datetime
import os

def dict2list(dic:dict):
	''' 将字典转化为列表 '''
	keys = dic.keys()
	vals = dic.values()
	lst = [(key, val) for key, val in zip(keys, vals)]
	return lst

def  calcaverage(list):
	sum = 0
	if len(list) == 0:
		return sum
	for v in list:
		try:
			sum += float(v)
		except Exception as e:
			continue
	return sum / len(list)

def save2csv(csvName,list):
	path = './datas/' + csvName + '.csv'
	if os.path.exists(path):
		os.remove(path)
	print(path)
	csvFile = open(path, 'w',encoding='utf-8',newline='')
	writer = csv.writer(csvFile)
	# writer.writerow(('日期','情感'))
	for l in list:
		writer.writerow(l)

def getstockemotions(stcok):
	datas = []
	datas2 = {}
	datas3 = []
	filepath = './sz50/'+stcok+'.csv'
	with open(filepath,"r",encoding="utf-8") as csvfile:
		#读取csv文件，返回的是迭代类型
		read = csv.reader(csvfile)	
		i = 0	
		for v in read:
			print(v[2]+","+v[3])
			datas.append([v[2],v[3]])
		
			i = i + 1
			if i == 1:
				datas3.append([v[2],v[3]])
				continue
			k = v[2]
			if k not in datas2.keys():
				datas2.setdefault(k,[])
			datas2[k].append(v[3])
			
	save2csv(stock,datas)

	for k in datas2.keys():
		datas3.append([k,calcaverage(datas2[k])])
	save2csv(stock+"_average",datas3)


xlsfile = r'sz50.xlsx' # 上证50股票名单
data = xlrd.open_workbook(xlsfile)
table = data.sheets()[0]          #通过索引顺序获取
# cols = table.col_values(2)
nrows = table.nrows
stocks = []
for i in range(nrows)[1:]:	
	stocks.append(table.cell(i,0).value)

for stock in stocks:
	try:
		print(stock)
		getstockemotions(stock)
	except:
		continue


	


'''
dates = {}
filepath = './datas/格力.csv'
with open(filepath,"r",encoding="utf-8") as csvfile:
	#读取csv文件，返回的是迭代类型
	read = csv.reader(csvfile)
	i = 0
	for k,v in read:
		i = i + 1
		if i == 1:
			continue
		print(v)
		if k not in dates.keys():
			dates.setdefault(k,[])
		dates[k].append(v)

dates2 = {}
for k in dates.keys():
	vs = dates[k]
	if(len(vs) == 0):
		continue
	sum = 0
	for v in vs:
		try:
			sum += float(v)
		except Exception as e:
			continue
	dates2.setdefault(k,sum/len(vs))

print('------------------------------------------------------\n')
for k in dates2.keys():
	print(str(k)+","+str(dates2[k]))
'''
