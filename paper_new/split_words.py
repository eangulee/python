import os
import csv
from snownlp import SnowNLP

def save2csv(csvName,list):
	path = './sz50/' + csvName + '.csv'
	if os.path.exists(path):
		os.remove(path)
	print(path)
	csvFile = open(path, 'w',encoding='utf-8',newline='')
	writer = csv.writer(csvFile)
	writer.writerow(('标题','帖子数','日期','情感'))
	for l in list:
		writer.writerow(l)

# filepath = 'comment_list.txt' # 评论
filepath = 'sz50_comment_list_2017_09_05_01_11_37_677425.txt' # 新闻
f = open(filepath,"r",encoding='utf-8')
lines = f.readlines() #读取全部内容
i = 0
stockname = ''
newcomments = []
total = len(lines)
for line in lines:
	if(line == '\n'):
		continue
	print(line)
	# if i > 100:
	# 	break
	line = line.replace('\n','') #去掉换行符
	contents = line.split(',')
	if(len(contents) > 1): #根据,号分割，长度大于1为评论内容，否则为股票名
		try:
			s = SnowNLP(contents[0])
			print(str(s.sentiments))
			contents.append(s.sentiments)
			print(contents)
			newcomments.append(contents)
		except:
			pass
	else:
		if(len(newcomments) > 0):
			save2csv(stockname,newcomments)
			newcomments.clear()
		stockname = line.split('.')[1] #取股票名字
		stockname = stockname.replace(':','')
		stockname = stockname.replace(u'\n','')
		print(stockname)
	i = i + 1
	if(i == total):# 最后一行
		save2csv(stockname,newcomments)