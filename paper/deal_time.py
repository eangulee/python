import re
import xlrd
import datetime
import time

def dict2list(dic:dict):
    ''' 将字典转化为列表 '''
    keys = dic.keys()
    vals = dic.values()
    lst = [(key, val) for key, val in zip(keys, vals)]
    return lst

filepath = 'sz50_comment_list_2017_09_06_03_25_52_881713.txt' # 评论
# filepath = 'sz50_comment_list_2017_09_06_03_25_52_881713.txt' # 新闻
f = open(filepath,"r",encoding='utf-8')
lines = f.readlines() #读取全部内容
dates = []

for line in lines:
	if(line == '\n'):
		continue
	# print(line)
	line = line.replace('\n','') #去掉换行符
	contents = line.split(',')
	if(len(contents) > 1): #根据,号分割，长度大于1为评论内容，否则为股票名
		try:
			dates.append(contents[len(contents) - 1])
		except:
			pass
monthdic = {}
daydic = {}
weekdaydic = {}
hourdic = {}

for datestr in dates:
	print(datestr)
	d = datetime.datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S")
	# print(d.year)
	month = d.month
	day = d.day 
	weekday = d.weekday() 
	hour = d.hour 
	if month not in monthdic.keys():
		monthdic.setdefault(month,1)
	monthcount = monthdic[month]
	monthcount = monthcount + 1
	monthdic[month] = monthcount

	if day not in daydic.keys():
		daydic.setdefault(day,1)
	daycount = daydic[day]
	daycount = daycount + 1
	daydic[day] = daycount

	if weekday not in weekdaydic.keys():
		weekdaydic.setdefault(weekday,1)
	weekdaycount = weekdaydic[weekday]
	weekdaycount = weekdaycount + 1
	weekdaydic[weekday] = weekdaycount

	if hour not in hourdic.keys():
		hourdic.setdefault(hour,1)
	hourcount = hourdic[hour]
	hourcount = hourcount + 1
	hourdic[hour] = hourcount

monthlist = sorted(dict2list(monthdic),key=lambda k:k[0],reverse=False)
daylist = sorted(dict2list(daydic),key=lambda k:k[0],reverse=False)
weekdaylist = sorted(dict2list(weekdaydic),key=lambda k:k[0],reverse=False)
hourlist = sorted(dict2list(hourdic),key=lambda k:k[0],reverse=False)

title = ''
content = ''
print('----------------------------------------month--------------------------------------')
for k in monthlist:
	title += str(k[0]) + ","
	content += str(k[1]) + ","
print(title)
print(content)

title = ''
content = ''
print('----------------------------------------day--------------------------------------')
for k in daylist:
	title += str(k[0]) + ","
	content += str(k[1]) + ","
print(title)
print(content)

title = ''
content = ''
print('----------------------------------------weekday--------------------------------------')
for k in weekdaylist:
	title += str(k[0]) + ","
	content += str(k[1]) + ","
print(title)
print(content)

title = ''
content = ''
print('----------------------------------------hour--------------------------------------')
for k in hourlist:
	title += str(k[0]) + ","
	content += str(k[1]) + ","
print(title)
print(content)