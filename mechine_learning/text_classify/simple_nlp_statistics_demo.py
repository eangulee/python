'''
Python 文本挖掘：简单的自然语言统计  
http://rzcoding.blog.163.com/blog/static/2222810172013102071131506/
'''
'''
# 1. 把文本变成双词搭配或三词搭配
import nltk

example_1 = ['I','am','a','big','apple','.']
example_bigrams = nltk.bigrams(example_1)
for e in example_bigrams:
	print(e)
example_trigrams = nltk.trigrams(example_1)
for e in example_trigrams:
	print(e)
'''
'''
# 2. 找语料库中出现频率最高的词
from nltk.probability import FreqDist

example_2 = ['I','am','a','big','apple','.','I','am','delicious',',','I','smells','good','.','I','taste','good','.']
fdist = FreqDist(word for word in example_2) #把文本转化成词和词频的字典

print(fdist.keys()) #词按出现频率由高到低排列
print(fdist.values()) #语料中每个词的出现次数倒序排列
'''
'''
# 3. 找信息量最丰富的词
import nltk
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

example_2 = ['I','am','a','big','apple','.','I','am','delicious',',','I','smells','good','.','I','taste','good','.']

bigrams = BigramCollocationFinder.from_words(example_2)

most_informative_chisq_bigrams = bigrams.nbest(BigramAssocMeasures.chi_sq, 3) #使用卡方统计法找
most_informative_pmi_bigrams = bigrams.nbest(BigramAssocMeasures.pmi, 3)  #使用互信息方法找

print(most_informative_chisq_bigrams)
print(most_informative_pmi_bigrams)
'''
'''
# 4. 统计不同词性的词的数量
import jieba.posseg

def postagger(sentence, para):
    pos_data = jieba.posseg.cut(sentence)
    pos_list = []
    for w in pos_data:
        pos_list.append((w.word, w.flag)) #make every word and tag as a tuple and add them to a list
    return pos_list


def count_adj_adv(all_review): #只统计形容词、副词和动词的数量
    adj_adv_num = []
    a = 0
    d = 0
    v = 0
    for review in all_review:
        pos = tp.postagger(review, 'list')
        for i in pos:
            if i[1] == 'a':
                a += 1
            elif i[1] == 'd':
                d += 1
            elif i[1] == 'v':
                v += 1
        adj_adv_num.append((a, d, v))
        a = 0
        d = 0
        v = 0
    return adj_adv_num
'''
'''
# 3. 使用nltk 计算信息熵和困惑值
# 信息熵有很多含义，当它和困惑值一起使用时，它们就有着特定的含义，
# 主要是表达一个信息的“惊奇度”（surprising）。
# 假设一个语料库，如果其中一条文本里面的内容和其它的其它文本差不多，
# 那它的熵和困惑值就很小。而如果一条文本的内容和其它文本差别很大，
# 这就很让人“惊奇”，此时它的熵和困惑值就大。
# nltk 中提供了计算信息熵和困惑值的方法。需要先用所有文本“训练”一个信息熵和困惑值模型，
# 再用这个“模型”计算每个文本的信息熵和困惑值。
from nltk.model.ngram import NgramModel

example_3 = [['I','am','a','big','apple','.'], ['I','am','delicious',','], ['I','smells','good','.','I','taste','good','.']]
train = list(itertools.chain(*example_3)) #把数据变成一个一维数组，用以训练模型

ent_per_model = NgramModel(1, train, estimator=None) #训练一元模型，该模型可计算信息熵和困惑值

def entropy_perplexity(model, dataset):
    ep = []
    for r in dataset:
        ent = model.entropy(r)
        per = model.perplexity(r)
        ep.append((ent, per))
    return ep

print(entropy_perplexity(ent_per_model, example_3))
'''