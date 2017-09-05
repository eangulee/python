#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __Author__: hong

#usage:python parse_station.py > stations.py


import re
import requests
from pprint import pprint
# pprint: 格式化输出
url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8971'
#获取URL
response = requests.get(url, verify=False)
#正则提取中文字母和代号
stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)
stations = dict(stations)
# indent:定义打印信息的缩进为4个空格
pprint(stations, indent=4)
pprint(dict(zip(stations.values(),stations.keys())))