# -*- coding: utf-8 -*-
"""Train tickets query via command-line.

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets beijing shanghai 2016-08-25
"""
from docopt import docopt
import requests
from stations import stations,stations_1
from prettytable import PrettyTable

class Colored(object):

    """Keep it simple, only use `red` and `green` color."""

    RED = '\033[91m'
    GREEN = '\033[92m'

    #: no color
    RESET = '\033[0m'

    def color_str(self, color, s):
        return '{}{}{}'.format(
            getattr(self, color),
            s,
            self.RESET
        )

    def red(self, s):
        return s
        # return self.color_str('RED', s)

    def green(self, s):
        return s
        # return self.color_str('GREEN', s)

class TrainCollection(object):

    # 显示车次、出发/到达站、 出发/到达时间、历时、一等坐、二等坐、软卧、动卧、硬卧、软坐、硬座、无座
    header = '车次 出发/到达站 出发/到达时间 历时 一等坐 二等坐 软卧 动卧 硬卧 软坐 硬座 无座'.split()
    

    def __init__(self, rows):
        self.rows = rows
        self.colored = Colored()

    # def _get_duration(self,row):
    #     """
    #     获取车次运行时间
    #     """
    #     duration = row.get('lishi').replace(':', 'h') + 'm'
    #     if duration.startswith('00'):
    #         return duration[4:]
    #     if duration.startswith('0'):
    #         return duration[1:]
    #     return duration

    # def colored(color, text):
    #     table = {
    #         'red': '\033[91m',
    #         'green': '\033[92m',
    #         # no color
    #         'nc': '\033[0'
    #     }
    #     cv = table.get(color)
    #     nc = table.get('nv')
    #     return ''.join([cv, text, nc])

    @property
    def trains(self):
        for row in self.rows:
            colums = row.split('|')
            train = [
                # 车次
                colums[3],
                # 出发、到达站
                '\n'.join([self.colored.green(stations_1.get(colums[6])), self.colored.red(stations_1.get(colums[7]))]),
                # 出发、到达时间
                '\n'.join([self.colored.green(colums[8]), self.colored.red(colums[9])]),
                # 历时
                colums[10],
                # 一等坐
                colums[31],
                # 二等坐
                colums[30],
                # 软卧
                colums[23],
                # 动卧
                colums[24],
                # 硬卧
                colums[28],
                # 软坐
                colums[25],
                # 硬坐
                colums[29],
                # 无座
                colums[26],
            ]
            yield train

    def pretty_print(self):
        """
        数据已经获取到了，剩下的就是提取我们要的信息并将它显示出来。
        `prettytable`这个库可以让我们它像MySQL数据库那样格式化显示数据。
        """
        pt = PrettyTable()
        # 设置每一列的标题
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        print(pt)
        # for row in self.rows:
        #     colums = row.split('|')
        #     print(colums)

def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    # print(arguments)
    from_staion = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    # print('from_staion:'+from_staion)
    # print('to_station:'+to_station)
    # print('date:'+date)
    
    # https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2017-07-20&leftTicketDTO.from_station=AOH&leftTicketDTO.to_station=NJH&purpose_codes=ADULT    
    # 构建URL
    url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(date, from_staion, to_station)
    # url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_station={}'.format(date, from_staion, to_station)
    print('url:' + url)
    # 添加verify=False参数不验证证书
    r = requests.get(url, verify=False)
    # print(r.text)
    # print(r.json())
    rows = r.json()['data']['result']
    trains = TrainCollection(rows)
    trains.pretty_print()

if __name__ == '__main__':
    cli()