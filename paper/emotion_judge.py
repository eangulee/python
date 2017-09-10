import re
import xlrd

def read_lines(filename):
    fp = open(filename, 'r',encoding='utf-8')
    lines = []
    for line in fp.readlines():
        line = line.strip()
        lines.append(line)
    fp.close()
    return lines

def getemotion(words,pos_dict,neg_dict):
	emotion = 0
	for w in words.split():
		if(w in pos_dict):
			emotion += 1
		if (w in neg_dict):
			emotion += -1
	return emotion

xlsfile = r'sz50.xlsx' # 上证50股票名单
data = xlrd.open_workbook(xlsfile)
table = data.sheets()[0]          #通过索引顺序获取
nrows = table.nrows
stocks = []
for i in range(nrows)[1:]:
	stock = str(table.cell(i,0).value)
	stocks.append(stock)

pos_dict = read_lines("pos_words.txt")
neg_dict = read_lines("neg_words.txt")

# for p in pos_dict:
# 	print(p)

# for p in neg_dict:
# 	print(p)

for stock in stocks[:1]:
	print(stock)
	# try:
	lines = read_lines('sz50/'+stock+"_split.txt")
	for l in lines:
		emotion = getemotion(l,pos_dict,neg_dict)
		print(l+"\t"+str(emotion))
	# except:
		# continue