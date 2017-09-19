import xlrd
import datetime

def save2csv(csvName,list):
	path = './comments/' + csvName + '.csv'
	if os.path.exists(path):
		os.remove(path)
	print(path)
	csvFile = open(path, 'w',encoding='utf-8',newline='')
	writer = csv.writer(csvFile)
	for l in list:
		writer.writerow(l)


stocks = ['工商银行','建设银行','交通银行','农业银行','浦发银行','招商银行']

datas = []
for stock in stocks:
	print(stock)
	xlsfile = r'./comments/'+ stock+".xlsx"
	data = xlrd.open_workbook(xlsfile)
	table = data.sheets()[0]          #通过索引顺序获取
	# cols = table.col_values(2)
	nrows = table.nrows
	for i in range(nrows)[1:]:
	stock = str(table.cell(i,1).value)
