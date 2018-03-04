# -*- coding: utf-8 -*-
import requests  
from bs4 import BeautifulSoup  
import traceback  
import re  
import datetime  
  
def getHTMLtext(url, code="utf-8"):  
	try:  
		r =requests.get(url)  
		r.raise_for_status()  
		r.encoding = code  
		# print("test")  
		return r.text  
	except:  
		return ""  
  
  
def getStockList(list,stockURL,filePath):  
	html = getHTMLtext(stockURL,"GB2312")  
	print("getstockList start")  
	soup = BeautifulSoup(html,'html.parser')  
	a = soup.find_all('a')  
	for i in a:  
		try:   
			# 过滤st和B股
			if 'ST' in i.text or 'B' in i.text:
				continue
			href = i.attrs['href']
			# s(h/z)加6位数字
			urls = re.findall(r"[s][hz][0367]\d{5}",href)
			# urls = re.findall(r"[s][hz]\d{6}",href)
			# print(urls)
			# list.append(re.findall(r"[s][hz]\d{6}",href)[0])  
			if len(urls) > 0:
				with open(filePath,'a',encoding='utf-8') as f:  
					f.write(i.text+'  '+urls[0] + '\n')  
				print(i.text+'  '+urls[0])
				list.append(urls[0])
		except:  
			continue  
  
  
def getStockInfo(list,stockURL,filePath):  
	count = 0  
	for stock in list:  
		url = stockURL + stock +".html"  
		html =getHTMLtext(url)  
		try:  
			if html=="":  
				continue  

			infoDict = {}  
			soup = BeautifulSoup(html,"html.parser")  
			stockInfo = soup.find('div',attrs={'class':'stock-bets'})  
  
			name = stockInfo.find_all(attrs={'class':'bets-name'})[0]  
			infoDict.update({'股票名称': name.next.split()[0]})  
			infoDict['股票代码'] = stock
  			
			keylist =stockInfo.find_all('dt')  
			vauleList = stockInfo.find_all('dd')  
			for i in range(len(keylist)):  
				key =keylist[i].text  
				vaule = vauleList[i].text  
				
				infoDict[key]= vaule  
			print(str(infoDict))
			with open(filePath,'a',encoding='utf-8') as f:  
				f.write(str(infoDict) + '\n')  
				count= count+1  
				print("\r当前进度: {:.2f}%".format(count*100/len(list)),end="")
		except:# IOError as e:
			count =count +1  
			print("\r当前进度: {:.2f}%".format(count*100/len(list)),end="")  
			continue  
  
  
  
def main():  
	print("start")  
	# 从东方财富获取股票列表
	stock_list_url='http://quote.eastmoney.com/stocklist.html'  
	# 从百度获取股票详情
	stock_info_url = 'https://gupiao.baidu.com/stock/'  
	# 数据保存路径
	time = re.sub(r'[^0-9]','_',str(datetime.datetime.now()))
	stocks_path = "data/stocks_{0}.txt".format(time)	
	print(stocks_path)
	slist=[]  
	getStockList(slist,stock_list_url,stocks_path)
	output_file = 'data/stock_info_{0}.txt'.format(time)
	print(output_file)
	getStockInfo(slist,stock_info_url,output_file)  
	print("end")  
  

if __name__ == '__main__':
	main()  