import jieba                                           #导入jieba模块
import re
import xlrd
# jieba.load_userdict("newdict.txt")                     #加载自定义词典  
import jieba.posseg as pseg 
import matplotlib as mpl
from nltk.probability import FreqDist
from nltk.text import Text
import jieba.analyse

#把停用词做成字典
stopwords = {}
fstop = open('stop_words.txt', 'r',encoding='utf-8')
for eachWord in fstop:
	stopwords[eachWord.strip()] = eachWord.strip()
fstop.close()

def splitSentence(inputFile, outputFile):
	# #把停用词做成字典
	# stopwords = {}
	# fstop = open('stop_words.txt', 'r',encoding='utf-8')
	# for eachWord in fstop:
	# 	stopwords[eachWord.strip()] = eachWord.strip()
	# fstop.close()

	fin = open(inputFile, 'r',encoding='utf-8')									#以读的方式打开文件  
	fout = open(outputFile, 'w',encoding='utf-8')								#以写得方式打开文件  
	# jieba.enable_parallel(4)									#并行分词
	for eachLine in fin:
		line = eachLine.strip()	#去除每行首尾可能出现的空格，并转为Unicode进行处理 
		line1 = re.sub("[0-9\s+\.\!\/_,$%^*()?;；:-【】+\"\']+|[+——！，;:。？、~@#￥%……&*（）]+", "",line)
		wordList = list(jieba.cut(line1))                        #用结巴分词，对每行内容进行分词  
		outStr = ''  
		for word in wordList:
			if word not in stopwords:  
				outStr += word  
				outStr += ' '  
		fout.write(outStr.strip() + '\n')       #将分词好的结果写入到输出文件
	fin.close()  
	fout.close()  
  
def getSentence(inputFile):
	sentence = ''
	try:
		fin = open(inputFile, 'r',encoding='utf-8')									#以读的方式打开文件  
		for eachLine in fin:
			line = eachLine.strip()	#去除每行首尾可能出现的空格，并转为Unicode进行处理 
			line1 = re.sub("[0-9\s+\.\!\/_,$%^*()?;；:-【】+\"\']+|[+——！，;:。？、~@#￥%……&*（）]+", "",line)
			# wordList = list(jieba.cut(line1))                        #用结巴分词，对每行内容进行分词  
			# outStr = ''  
			# for word in wordList:
			# 	if word not in stopwords:  
			# 		outStr += word  
			# 		outStr += ' '  
			sentence += line1.strip()+"\n"
		fin.close()  
	except:
		print('there is a mistak in {}'.format(inputFile))

	return sentence
  


# splitSentence('ss.txt', 'tt.txt')

xlsfile = r'sz50.xlsx' # 上证50股票名单
data = xlrd.open_workbook(xlsfile)
table = data.sheets()[0]          #通过索引顺序获取
# cols = table.col_values(2)
nrows = table.nrows
stocks = []
for i in range(nrows)[1:]:
	stock = str(table.cell(i,0).value)
	stocks.append(stock)

words = ''
for stock in stocks:
	print(stock)
	try:
		# splitSentence('sz50/'+stock+".txt",'sz50/'+stock+"_split.txt")
		words += getSentence('sz50/'+stock+".txt")+"\n"
	except:
		continue

tags = jieba.analyse.extract_tags(words,topK=100)
for t in tags:
	print(t)

# print(words)
# print('-------------------------------------------------------------------------------------------')
# texts = jieba.cut(words)                        #用结巴分词，对每行内容进行分词  
# # print(texts)

# # print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

# text = Text(texts)
# fdist1 = FreqDist(text)
# print(fdist1)
# print(fdist1.N())
# print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
# vocabulary1 = list(fdist1.keys())
# sortedvocabulary = []
# for v in vocabulary1:
#     # print(v+"\t"+str(fdist1[v]))
#     if v not in stopwords:
#     	sortedvocabulary.append((v,fdist1[v]))

# sortedvocabulary = sorted(sortedvocabulary,key=lambda item:item[1],reverse=True)

# for k in sortedvocabulary:
# 	print(k[0]+"\t"+str(k[1]))
# 	# print(k)

# for sample in fdist1:
# 	print(sample)
# fdist1.tabulate()
# fdist1.plot()