import requests
from bs4 import BeautifulSoup
import os
import time
import csv

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.1708.400 QQBrowser/9.5.9635.400'
}

def getHTMLtext(url, code="utf-8"):  
	try:  
		r =requests.get(url)  
		r.raise_for_status()  
		r.encoding = code  
		# print(r.text)  
		return r.text  
	except:  
		return "" 

# parameter
# shareCode/year/season : num ,
def sharesCrawl(shareCode,year,season):
	# shareCodeStr = str(shareCode)
	yearStr = str(year)
	seasonStr = str(season)
	url = 'http://quotes.money.163.com/trade/lsjysj_'+shareCode+'.html?year='+yearStr+'&season='+seasonStr
	print(url)
	data = requests.get(url, headers=headers)
	soup = BeautifulSoup(data.text, 'html.parser')

	table = soup.findAll('table',class_='table_bg001')[0]
	rows = table.findAll('tr')

	return rows[::-1]


def writeCSVWithName(shareCode,name,beginYear,endYear):
	# shareCodeStr = str(shareCode)

	# url = 'http://quotes.money.163.com/trade/lsjysj_' + shareCode + '.html'
	# print(url)
	# data = requests.get(url, headers=headers)
	# soup = BeautifulSoup(data.text, 'html.parser')
	csvpath = './dataWithName/' + name + '.csv'
	if(os.path.exists(csvpath)):
		os.remove(csvpath)
	csvFile = open(csvpath, 'w',encoding='utf8',newline='')	
	writer = csv.writer(csvFile)
	writer.writerow(('日期','开盘价','最高价','最低价','收盘价','涨跌额','涨跌幅','成交量','成交金额','振幅','换手率'))

	
	for i in range(beginYear, endYear + 1):
		try:
			# print (str(i) + ' is going')
			# time.sleep(4)
			for j in range(1, 5):
				rows = sharesCrawl(shareCode,i,j)
				for row in rows:
					csvRow = []
					for cell in row.findAll('td'):
						csvRow.append(cell.get_text().replace(',',''))
					if csvRow != []:
						writer.writerow(csvRow)
				# time.sleep(3)
				# print(str(i) + '年' + str(j)  + '季度is done')
		except Exception as e:
			print(e)
			continue
	csvFile.close()

# 读取csv至字典 
csvpath = r'D:\python\paper\sz50.csv' # 上证50股票名单
csvFile = open(csvpath, "r",encoding='utf-8')
reader = csv.reader(csvFile)
# 建立空字典 
stocks = []
stockdic = {}
for item in reader:
	# 忽略第一行
	if reader.line_num == 1:
		continue
	stocks.append(str(item[1]))
	stockdic[str(item[1])] = item[0]    
	# print(item)
csvFile.close()

i = 0
for k in stocks:
	if(i >= 100):
		break
	writeCSVWithName(k,stockdic[k],2007,2017)
	# print(k+","+stockdic[k])
	i = i + 1
