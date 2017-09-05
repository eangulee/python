# encoding=utf-8
import sys
import matplotlib as mpl
import jieba
from nltk.probability import FreqDist
from nltk.text import Text
from matplotlib.font_manager import FontProperties

# default_encoding = sys.getfilesystemencoding()
# font family
# msyh = FontProperties('msyh')
msyh = FontProperties(fname=r"/Users/eangulee/anaconda3/lib/python3.6/site-packages/matplotlib/mpl-data/fonts/ttf/msyh.ttf")

jieba.suggest_freq(('计算机', '相关'), True)

text1 = "小明硕士毕业于中国科学院计算所，小明后在日本京都大学深造，小明接着又回到中国科学院计算所，小明在中国科学院计算所任硕士研究生导师，小明做计算机相关研究。"
seg_list = jieba.cut(text1)
text = Text(seg_list)
fdist1 = FreqDist(text)
# print(fdist1)
# vocabulary1 = list(fdist1.keys())
# for v in vocabulary1:
#     print(v)
print(fdist1.max())
print(fdist1['中国科学院'])
print(fdist1.freq('硕士'))
# 绘制频率分布表
fdist1.tabulate()
# 绘制频率分布图
# 处理中文标题
# http://blog.csdn.net/u013038499/article/details/52449768
# http://www.cnblogs.com/morya/p/4304894.html 
fdist1.plot(fontproperties=msyh,title='亲爱的，我想你')
# fdist1.plot()