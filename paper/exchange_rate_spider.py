import requests
import re
from bs4 import BeautifulSoup
import datetime
import os
import csv

def save2csv(csvName,list):
	path = './exchange_rate/' + csvName + '.csv'
	if os.path.exists(path):
		os.remove(path)
	print(path)
	csvFile = open(path, 'w',encoding='utf-8',newline='')
	writer = csv.writer(csvFile)
	for l in list:
		writer.writerow(l)

def getHTMLtext(url, code="utf-8"):  
	try:  
		r =requests.get(url)  
		r.raise_for_status()  
		r.encoding = code  
		# print(r.text)  
		return r.text  
	except:  
		return "" 

searchurl = 'http://fx.cmbchina.com/Hq/History.aspx?startdate=2009-01-01&enddate=2017-09-06&nbr=%u7F8E%u5143&type=days'
searchhtml = getHTMLtext(searchurl)
searchsoup = BeautifulSoup(searchhtml,'html.parser')
searchdiv  = searchsoup.find_all('div',class_='goTextInput')[0]
pagestr = searchdiv.text.split('/')[1]
pagestr = pagestr.replace('页','')
page = int(pagestr)

print(page)

for i in range(page)[0:]:	
	url = 'http://fx.cmbchina.com/Hq/History.aspx?nbr=美元&startdate=2009-01-01&enddate=2017-09-06&page={}'.format(i+1)
	html = getHTMLtext(url)
	soup = BeautifulSoup(html,'html.parser')
	tbody = soup.find_all('tbody')[1]
	trs = tbody.find_all('tr')

	lines = []
	lines.append(['日期','汇买价(元)','钞买价(元)','汇卖价(元)','钞卖价(元)','中间价'])
	for tr in trs:
		print(tr)
		tds = tr.find_all('td')
		line = []
		for td in tds:
			v = td.text
			v = v.replace('年','-')
			v = v.replace('月','-')
			v = v.replace('日','')
			line.append(v)
		lines.append(line)

time = re.sub(r'[^0-9]','_',str(datetime.datetime.now()))
csvname = 'exchange_rate_{}'.format(time)
save2csv(csvname,lines)