import jieba                                           #导入jieba模块
import re
import jieba.posseg as pseg 
from nltk.probability import FreqDist
from nltk.text import Text
import jieba.analyse

#把停用词做成字典
stopwords = {}
fstop = open('datas/stop_words.txt', 'r',encoding='utf-8')
for eachWord in fstop:
	stopwords[eachWord.strip()] = eachWord.strip()
fstop.close()

def splitwords(inputFile, outputFile):
	fin = open(inputFile, 'r',encoding='utf-8')#以读的方式打开文件  
	fout = open(outputFile, 'w',encoding='utf-8')#以写得方式打开文件  
	# jieba.enable_parallel(4)#并行分词
	words = []
	wordsstr = ''
	for eachLine in fin:
		line = eachLine.strip()	#去除每行首尾可能出现的空格，并转为Unicode进行处理 
		line1 = re.sub("[0-9\s+\.\!\/_,$%^*()?;；:-【】+\"\']+|[+——！，;:。？、~@#￥%……&*（）]+", "",line)
		wordList = list(jieba.cut(line1))                        #用结巴分词，对每行内容进行分词  
		for word in wordList:
			if word not in stopwords:
				if(word not in words):# 去重
					words.append(word)
					wordsstr += word  
					wordsstr += ' '
	fout.write(wordsstr.strip())#将分词好的结果写入到输出文件
	fin.close()  
	fout.close()
	return words


def getsentence(inputFile, outputFile):
	fin = open(inputFile, 'r',encoding='utf-8')#以读的方式打开文件  
	fout = open(outputFile, 'w',encoding='utf-8')#以写得方式打开文件  
	# jieba.enable_parallel(4)#并行分词
	sentences = []
	for eachLine in fin:
		line = eachLine.strip()	#去除每行首尾可能出现的空格，并转为Unicode进行处理 
		line1 = re.sub("[0-9\s+\.\!\/_,$%^*()?;；:-【】+\"\']+|[+——！，;:。？、~@#￥%……&*（）]+", "",line)
		wordList = list(jieba.cut(line1))                        #用结巴分词，对每行内容进行分词  
		wordsstr = ''
		for word in wordList:
			if word not in stopwords:
				wordsstr += word
				wordsstr += ' '
				sentences.append(wordsstr)
			fout.write(outStr.strip() + '\n')#将分词好的结果写入到输出文件
	fin.close()  
	fout.close()
	return sentences


splitwords('datas/pos.txt','datas/pos_feature.txt')
splitwords('datas/neg.txt','datas/neg_feature.txt')