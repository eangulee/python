from nltk.book import *
# from __future__ import division

'''
print(text1)
print(text2)

# 搜索文本
monstrous = text1.concordance("monstrous")
print(monstrous)
lived = text3.concordance("lived")
print(lived)
'''
'''
# 相似度
test1_monstrous_similar = text1.similar("monstrous")
print(test1_monstrous_similar)

test2_monstrous_similar = text2.similar("monstrous")
print(test2_monstrous_similar)

# 函数common_contexts允许我们研究两个或两个以上的词共同的上下文
text2_common_contexts = text2.common_contexts(["monstrous", "very"])
print(text2_common_contexts)
'''

# '''
# 离散图
# text4.dispersion_plot(["citizens", "democracy", "freedom", "duties", "America"])
# '''

'''
# 计数词汇
print(len(text3))
# 统计出现词的个数 set
print(len(set(text3)))
set1 = sorted(set(text3))
print(set1)


r = len(text3) / len(set(text3))
print(r)
print(text3.count('smote'))
r = 100 * text4.count('a') / len(text4)
print(r)

idx = text4.index('awaken')
print(idx)
'''

# 简单的统计
saying = ['After', 'all', 'is', 'said', 'and', 'done', 'more', 'is', 'said', 'than', 'done']
tokens = set(saying)
tokens = sorted(tokens)
print(tokens[-2:])

# 获取最常见的50个标识符
fdist1 = FreqDist(text1)
print(fdist1)
vocabulary1 = list(fdist1.keys())
# print(type(vocabulary1))
print(vocabulary1[:50])

# 只出现一次的标识符
print(fdist1.hapaxes())

# 累计占有50%的标识符，作图
fdist1.plot(50, cumulative=True)	

