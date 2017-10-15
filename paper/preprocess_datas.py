'''
将nlpir的分词进行处理
'''
import xlrd
import re

#把停用词做成字典
stopwords = {}
fstop = open('split/stop_words.txt', 'r',encoding='utf-8')
for eachWord in fstop:
	stopwords[eachWord.strip()] = eachWord.strip()
fstop.close()

def splitwords(inputFile, outputFile):
	fin = open(inputFile, 'r',encoding='utf-8')#以读的方式打开文件  
	fout = open(outputFile, 'w',encoding='utf-8')#以写得方式打开文件  
	words = []
	for eachLine in fin:
		# print(eachLine == ' \n')
		if(eachLine == '' or eachLine == ' \n' or eachLine == '\n'):
			continue
		wordList = eachLine.split()
		wordsstr = ''
		for word in wordList:
			for removeword in removewords:
				word = word.replace(removeword,'')
			if word not in stopwords:
				# if(word not in words):# 去重
				# 	words.append(word)
					wordsstr += word  
					wordsstr += ' '
		words.append(wordsstr.strip())
		fout.write(wordsstr.strip()+"\n")#将分词好的结果写入到输出文件
	fin.close()  
	fout.close()
	return words

def getsentence(path):
	f = open(path, 'r',encoding='utf-8')#以读的方式打开文件  
	sentences = []
	for eachLine in f:
		eachLine = eachLine.replace('\n','')
		sentences.append(eachLine)
	f.close()
	return sentences

xlsfile = r'D:\python\paper\sz50.xlsx' # 上证50股票名单
data = xlrd.open_workbook(xlsfile)
table = data.sheets()[0]          #通过索引顺序获取
# cols = table.col_values(2)
nrows = table.nrows
stocks = []
for i in range(nrows)[1:]:
	stocks.append(table.cell(i,0).value)

#去除词性标识
removewords = getsentence('split/词性符号.txt')
removewords = sorted(removewords,key=lambda removeword: len(removeword), reverse=True)
# for r in removewords:
# 	print(r)

for stock in stocks:
	print(stock)
	splitwords("split/"+stock+".txt","split/"+stock+"_split.txt")