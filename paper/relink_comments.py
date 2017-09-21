import xlrd
import datetime
import csv
import os

def save2csv(csvName,list):
	path = csvName
	if os.path.exists(path):
		os.remove(path)
	print(path)
	csvFile = open(path, 'w',encoding='utf-8',newline='')
	writer = csv.writer(csvFile)
	for l in list:
		writer.writerow(l)

def getcsv(csvname):
	lines = []
	open_file = open(csvname, 'r',encoding='utf-8')
	csv_reader = csv.reader(open_file)
	for row in csv_reader:
		lines.append(row)
	return lines

def getline(key,lines):
	for line in lines:
		# if(len(str(line[0])) == len(key)):
		# print(str(line[0]).strip()+"|"+key.strip())
		if(str(line[0]).strip() == key.strip()):
			return line
	return []


# stocks = ['工商银行','建设银行','交通银行','农业银行','浦发银行','招商银行']
stocks = ['工商银行','农业银行','浦发银行',]

datas = {}
for stock in stocks:
	lines = []
	xlsfile = r'./comments/'+ stock+".xlsx"
	data = xlrd.open_workbook(xlsfile)
	table = data.sheets()[0]          #通过索引顺序获取
	# cols = table.col_values(2)
	nrows = table.nrows
	for i in range(nrows)[1:]:
		title = table.cell(i,0).value
		tag = table.cell(i,1)
		number = table.cell(i,2)
		# d = xlrd.xldate.xldate_as_datetime(table.cell(i,0).value,0)	
		# dstr = d.strftime('%Y-%m-%d %h-%m-%s')
		emotion = table.cell(i,4)
		line = []
		line.append(title)
		line.append(tag)
		line.append(number)
		line.append(emotion)
		lines.append(line)

	# print(stock+":"+str(len(lines)))
	datas.setdefault(stock,lines)


datas2 = {}
for stock in stocks:
	lines = getcsv('./comments/original1/'+stock+".csv")
	# print(stock+":"+str(len(lines)))
	datas2.setdefault(stock,lines)

datas3 = {}
for k in datas.keys():
	lines = datas[k]
	newlines = []
	for line in lines:
		lines2 = datas2[k]
		l = getline(str(line[0]),lines2)
		# print(str(line[0])+":"+str(len(l)))
		if(len(l)>0):
			lines2.remove(l)
			datas2[k] = lines2
			# newline = str(line[0])+","+str(line[1])+","+str(line[2])+","+str(l[3])+","+str(l[4])+","+str(l[5])
			newline = []
			newline.append(str(line[0]))#标题
			newline.append(str(line[1]))#tag
			newline.append(str(line[2]))#帖子数
			newline.append(str(l[3]))#字数
			newline.append(str(l[4]))#影响力
			newline.append(str(l[5]))#时间
			newlines.append(newline)
	save2csv('./comments/'+k+".csv",newlines)



