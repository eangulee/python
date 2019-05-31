# coding:utf-8
import requests
from bs4 import BeautifulSoup
import os
import time


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.1708.400 QQBrowser/9.5.9635.400'
}
#获取历年成交量
url = 'http://quotes.money.163.com/trade/lsjysj_zhishu_000001.html?year=2009&season=4'


# parameter
# shareCode/year/season : num ,
def sharesCrawl(shareCode,year,season):
    shareCodeStr = shareCode
    yearStr = str(year)
    seasonStr = str(season)
    url = 'http://quotes.money.163.com/trade/lsjysj_zhishu_'+shareCodeStr+'.html?year='+yearStr+'&season='+seasonStr

    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'lxml')
    # print soup
    title = soup.select('h1.name > a')[0].get_text()

    stockData = soup.select('div.inner_box > table > tr > td')

    if os.path.exists('./'+shareCodeStr+title) == False:
        #create the share folder
        os.mkdir('./'+shareCodeStr+title)

    f = open('./'+shareCodeStr+title+'/Y'+yearStr+'S'+seasonStr+'.txt','wb')
    for index,value in enumerate(stockData):
        if index % 11 == 10:
            f.write(value.get_text()+'\n')
        else:
            f.write(value.get_text() +'\t')
    f.close()

# sharesCrawl(600019,'2016','2')



def sharesCrawl2(shareCode,year,season):
    shareCodeStr = shareCode
    yearStr = str(year)
    seasonStr = str(season)
    url = 'http://quotes.money.163.com/trade/lsjysj_zhishu_' + shareCodeStr + '.html?year=' + yearStr + '&season=' + seasonStr
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'lxml')
    stockData = soup.select('div.inner_box > table > tr > td')
    resultString = ''
    for index, value in enumerate(stockData):
        if index % 9 == 8:
            resultString += value.get_text() + '\n'
        else:
            resultString += value.get_text() + '|'
    return resultString

# print sharesCrawl2(600019,2016,2)



def createUrl(shareCode,beginYear,endYear):
    shareCodeStr = shareCode

    # if os.path.exists('./'+title) == False:
    #     #create the share folder
    #     os.mkdir('./'+title)

    f = open('./' + shareCodeStr + '.txt', 'w+')

    for i in range(beginYear,endYear+1):
        # print i
        # time.sleep(5)
        for j in range(1,5):
            txt = sharesCrawl2(shareCode,i,j)
            print(txt)
            f.write(txt + '\n ------- '+str(i)+'/'+str(j)+'----------------\n')
            time.sleep(1)
    try:
        pass
    except:
        print('----- 爬虫出错了！没有进入循环-----')
    finally:
        f.close()
#000001 上证指数
#399300 沪深300
createUrl('399300',1990,2019)


"""
body > div.area > div.inner_box > table > tbody > tr:nth-child(1) > td:nth-child(1)
body > div.area > div.header > div.stock_info > table > tbody > tr > td.col_1 > h1 > a
"""