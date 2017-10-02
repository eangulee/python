import xlrd
import requests
import re
from bs4 import BeautifulSoup
import math
import datetime

def getHTMLtext(url, code="utf-8"):  
	try:  
		r =requests.get(url)  
		r.raise_for_status()  
		r.encoding = code  
		# print(r.text)  
		return r.text  
	except:  
		return "" 

def dict2list(dic:dict):
    ''' 将字典转化为列表 '''
    keys = dic.keys()
    vals = dic.values()
    lst = [(key, val) for key, val in zip(keys, vals)]
    return lst

# xlsfile = r'D:\python\paper\sz50.xlsx' # 上证50股票名单
# data = xlrd.open_workbook(xlsfile)
# table = data.sheets()[0]          #通过索引顺序获取
# # cols = table.col_values(2)
# nrows = table.nrows
# stocks = []
# stocks2 = {}
# for i in range(nrows)[1:]:
# 	stock = str(table.cell(i,1).value)
# 	stock = stock.replace('.0','')
# 	if(len(stock) < 6):# 股票代码为6位
# 		diff = 6 - len(stock)
# 		for j in range(diff):
# 			stock = '0' + stock
# 	# print(stock)
# 	stocks.append(stock)
# 	stocks2.setdefault(stock,table.cell(i,0).value)
# for k in stocks2.keys():
# 	print(k+":"+stocks2[k])
stocks = ['601939','601288','601398','601328','600000','600036']
# stocks = ['601988']
stocks2 ={'601939':'建设银行','601288':'农业银行','601398':'工商银行','601328':'交通银行','600000':'浦发银行','600036':'招商银行'}
# stocks2 = {'601988':'中国银行'}
commentCounts = {}
i = 1
for st in stocks[0:]:
	url = 'http://guba.eastmoney.com/list,{},99.html'.format(st)
	print(str(i)+'.url:' + url)
	i = i + 1
	html = getHTMLtext(url)
	soup = BeautifulSoup(html,'html.parser')
	spans = soup.find_all('span',class_='pagernums')
	try: 
		dataPager = spans[0].attrs['data-pager']
		total = dataPager.split('|')[1]
		# print(total)
		commentCounts.setdefault(str(st),int(total))
	except:
		continue
		
commentCounts = sorted(dict2list(commentCounts), key=lambda d:d[1], reverse = True)
stockPages = {} # 股票总页数字典
# print(len(commentCounts))
print('stock comment count sorted:')
print('股票代码,股票名称,总帖子数,总页数')
for k in commentCounts:
	name = stocks2[k[0]]
	# print(name)
	total = k[1]
	page = total / 80
	page = math.ceil(page)
	print(k[0]+","+name+","+str(total)+","+str(page))
	stockPages.setdefault(k[0],page)

i = 0
commenturls = {} # 评论链接字典
comments = {} # 评论标题字典
# 请求所有分页链接
for k in stockPages.keys():
	if i >= 50:
		break
	page = stockPages[k]		
	print('get stock:'+str(i+1)+'.'+ k)
	urls = []
	titles = []
	for j in range(page):
		url = 'http://guba.eastmoney.com/list,{},99_{}.html'.format(k,j+1)
		print(str(j+1)+'.url:' + url)
		html = getHTMLtext(url)
		soup = BeautifulSoup(html,'html.parser')
		divs = soup.find_all('div',class_='articleh')
		for div in divs:
			try:
				# print(div)
				link = div.find_all('a')[0]
				read = div.find_all('span',class_="l1")[0]
				feedback = div.find_all('span',class_="l2")[0]
				href = link.attrs['href']
				# time = div.find_all('span',class_="l6")[0]
				# print('read:'+str(read.text))
				commenturl = 'http://guba.eastmoney.com{}'.format(href)

				# 获取发帖时间
				commenthtml = getHTMLtext(commenturl)
				commentsoup = BeautifulSoup(commenthtml,'html.parser')
				datestr = commentsoup.find_all('div',class_='zwfbtime')[0]
				# print(datestr.text)
				datestr = datestr.text[4:23]
				zwcontentmain = commentsoup.find_all('div',class_='zwcontentmain')[0]
				zwcontentmainstr = zwcontentmain.text.strip()
				# print('zwcontentmain:'+zwcontentmainstr)

				# 获取发帖用户信息
				zwconttbndiv = commentsoup.find_all("div",id='zwconttbn')[0]
				# print(zwconttbndiv.prettify())
				span = zwconttbndiv.find_all('span')[0]
				uid = span.attrs['data-uid']
				# print(uid)
				userurl = 'http://iguba.eastmoney.com/{}'.format(uid)
				userhtml = getHTMLtext(userurl)
				usersoup = BeautifulSoup(userhtml,'html.parser')

				userdiv = usersoup.find_all('div',id='influence')[0]
				# print(userdiv.prettify())
				userspan = userdiv.find_all('span')[0]
				influencestr = userspan.attrs['data-influence']
				influence = float(influencestr) / 2
				print(influence) 

				# http://iguba.eastmoney.com/
				# for span in spans:
				# 	print(span.prettify())
				# 	spanclass = span.attrs['class']
				# 	# <span class="stars stars35"></span>
				# 	if('stars stars' in spanclass):
				# 		# print(spanclass)
				# 		star = spanclass.replace('stars stars','')
						# print(star)
				# for span in spans:
				# 	print(span.text)
				# print(influence)
				# spans = influence.find_all('span')
				# print(len(spans))

				# classstr = stars.attrs['class']
				# print(classstr)
				# print('stars:'+str(classstr[-1]))

				# print(datestr)
				line = link.text.replace(',',"，")+","+read.text+","+feedback.text+","+str(len(zwcontentmainstr))+","+str(influence)+","+datestr
				# print(line)
				titles.append(line)
				urls.append(commenturl)
			except Exception as e:
				print(e)
				continue
	comments.setdefault(k,titles)
	commenturls.setdefault(k,urls)
	i = i + 1

time = re.sub(r'[^0-9]','_',str(datetime.datetime.now()))
output_file = u'D:\python\python\paper\sz50_comment_list_{0}.txt'.format(time)
print(output_file)

i = 1
with open(output_file,'a',encoding='utf-8') as f:
	for k in comments.keys():
		titles = comments[k]
		name = stocks2[k]
		f.write('{}.{}:'.format(i,name) + '\n')
		f.write('标题,阅读,评论,字数,影响力,时间\n')
		for title in titles:
			f.write(title + '\n')
		f.write('\n')
		i = i + 1