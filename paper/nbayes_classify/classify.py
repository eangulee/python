
def getuptag(words):
	return dict(())

xlsfile = r'D:\python\python\paper\nbayes_classify\浦发银行股评判断.xlsx'
data = xlrd.open_workbook(xlsfile)
table = data.sheets()[0]          #通过索引顺序获取
# cols = table.col_values(2)
nrows = table.nrows
traindata = []
for i in range(nrows)[2:]:
	stock = str(table.cell(i,1).value)
	
	stocks.append(stock)
	stocks2.setdefault(stock,table.cell(i,2).value)
