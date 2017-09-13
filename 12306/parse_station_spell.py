#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __Author__: lily

import re
import requests
from pprint import pprint
# pprint: 格式化输出
url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8971'
#获取URL
response = requests.get(url, verify=False)
stations = re.findall(r'([A-Z]+)\|([a-z]+)', response.text)
stations = dict(stations)
# 将keys和values互换组成一个新的字典
stations = dict(zip(stations.values(), stations.keys()))
pprint(stations, indent=4)