'''
Python 文本挖掘：使用机器学习方法进行情感分析（介绍）  
http://rzcoding.blog.163.com/blog/static/22228101720131019104850984/
Python 文本挖掘：使用机器学习方法进行情感分析（原理）  
http://rzcoding.blog.163.com/blog/static/222281017201310193504714/
Python 文本挖掘：使用机器学习方法进行情感分析（一、特征提取和选择）  
http://rzcoding.blog.163.com/blog/static/2222810172013102003555556/
Python 文本挖掘：使用机器学习方法进行情感分析（二、分割数据及赋予类标签） 
http://rzcoding.blog.163.com/blog/static/22228101720131020125628/
Python 文本挖掘：使用机器学习方法进行情感分析（三、分类器及其准确度）  
http://rzcoding.blog.163.com/blog/static/2222810172013102093539248/
Python 文本挖掘：使用机器学习方法进行情感分析（四、使用分类器进行分类）  
http://rzcoding.blog.163.com/blog/static/22228101720131020105621180/
'''
import nltk
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist
from random import shuffle
import sklearn
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle

# 用于字典排序
def dict2list(dic:dict):
	''' 将字典转化为列表 '''
	keys = dic.keys()
	vals = dic.values()
	lst = [(key, val) for key, val in zip(keys, vals)]
	return lst

def switch(list):
	result = []
	for l in list:
		for w in l:
			result.append(w)
	return result

# Python 文本挖掘：使用机器学习方法进行情感分析（一、特征提取和选择）
# 把所有词作为特征
def bag_of_words(words):	
	return dict([(word, True) for word in words])

def bag_of_word(word):
	return dict([(word, True)])

# 把双词搭配（bigrams）作为特征
def bigram(words, score_fn = BigramAssocMeasures.chi_sq, n=1000):
	bigram_finder = BigramCollocationFinder.from_words(words)  #把文本变成双词搭配的形式
	bigrams = bigram_finder.nbest(score_fn, n) #使用了卡方统计的方法，选择排名前1000的双词
	return bag_of_words(bigrams)

# 把所有词和双词搭配一起作为特征
def bigram_words(words, score_fn = BigramAssocMeasures.chi_sq, n=1000):
	bigram_finder = BigramCollocationFinder.from_words(words)
	bigrams = bigram_finder.nbest(score_fn, n)
	newwords = []
	for word in words:
		newwords.append((word,))
	# for b in bigrams:
	# 	print(b)
	return bag_of_words(newwords + bigrams)  #所有词和（信息量大的）双词搭配一起作为特征

# 计算整个语料里面每个词的信息量
def create_word_scores(posWords,negWords):
	# posWords = pickle.load(open('D:/code/sentiment_test/pos_review.pkl','r'))
	# negWords = pickle.load(open('D:/code/sentiment_test/neg_review.pkl','r'))

	# posWords = list(itertools.chain(*posWords)) #把多维数组解链成一维数组
	# negWords = list(itertools.chain(*negWords)) #同理
	posWords = switch(posWords)
	negWords = switch(negWords)

	word_fd = FreqDist() #可统计所有词的词频
	cond_word_fd = ConditionalFreqDist() #可统计积极文本中的词频和消极文本中的词频
	for word in posWords:
		# print(word)
		word_fd[word] += 1
		cond_word_fd['pos'][word] += 1
	for word in negWords:
		word_fd[word] += 1
		cond_word_fd['neg'][word] += 1

	pos_word_count = cond_word_fd['pos'].N() #积极词的数量
	neg_word_count = cond_word_fd['neg'].N() #消极词的数量
	total_word_count = pos_word_count + neg_word_count
	print("pos_word_count:"+str(pos_word_count))
	print("neg_word_count:"+str(neg_word_count))

	word_scores = {}
	# for k in word_fd.dict2list():
		# word = k[0]
		# freq = k[1]
	for word in word_fd.keys():
		freq = word_fd[word]
		pos_score = BigramAssocMeasures.chi_sq(cond_word_fd['pos'][word], (freq, pos_word_count), total_word_count) #计算积极词的卡方统计量，这里也可以计算互信息等其它统计量
		neg_score = BigramAssocMeasures.chi_sq(cond_word_fd['neg'][word], (freq, neg_word_count), total_word_count) #同理
		word_scores[word] = pos_score + neg_score #一个词的信息量等于积极卡方统计量加上消极卡方统计量

	return word_scores #包括了每个词和这个词的信息量

# 计算整个语料里面每个词和双词搭配的信息量
def create_word_bigram_scores(posWords,negWords):
	# posdata = pickle.load(open('D:/code/sentiment_test/pos_review.pkl','r'))
	# negdata = pickle.load(open('D:/code/sentiment_test/neg_review.pkl','r'))
	
	# posWords = list(itertools.chain(*posdata))
	# negWords = list(itertools.chain(*negdata))

	posWords = switch(posWords)
	negWords = switch(negWords)

	bigram_finder = BigramCollocationFinder.from_words(posWords)
	bigram_finder = BigramCollocationFinder.from_words(negWords)
	posBigrams = bigram_finder.nbest(BigramAssocMeasures.chi_sq, 5000)
	negBigrams = bigram_finder.nbest(BigramAssocMeasures.chi_sq, 5000)

	pos = posWords + posBigrams #词和双词搭配
	neg = negWords + negBigrams

	word_fd = FreqDist()
	cond_word_fd = ConditionalFreqDist()
	for word in pos:
		word_fd[word] += 1
		cond_word_fd['pos'][word] += 1
	for word in neg:
		word_fd[word] += 1
		cond_word_fd['neg'][word] += 1

	pos_word_count = cond_word_fd['pos'].N()
	neg_word_count = cond_word_fd['neg'].N()
	total_word_count = pos_word_count + neg_word_count

	word_scores = {}
	# for k in word_fd.dict2list():
	# 	word = k[0]
	# 	freq = k[1]
	for word in word_fd.keys():
		freq = word_fd[word]
		pos_score = BigramAssocMeasures.chi_sq(cond_word_fd['pos'][word], (freq, pos_word_count), total_word_count)
		neg_score = BigramAssocMeasures.chi_sq(cond_word_fd['neg'][word], (freq, neg_word_count), total_word_count)
		word_scores[word] = pos_score + neg_score

	return word_scores

# 根据信息量进行倒序排序，选择排名靠前的信息量的词
def find_best_words(word_scores, number):
	#把词按信息量倒序排序。number是特征的维度，是可以不断调整直至最优的
	best_vals = sorted(dict2list(word_scores), key=lambda d:d[1], reverse=True)[:number]
	print(type(best_vals))
	best_words = set([w for w,s in best_vals])
	return best_words

# 把选出的这些词作为特征（这就是选择了信息量丰富的特征）
# def best_word_features(words,best_words):
# 	return dict([(word, True) for word in words if word in best_words])
def best_word_features(words,best_words):
	return [word for word in words if word in best_words]

# test
# word_scores_1 = create_word_scores()
# word_scores_2 = create_word_bigram_scores()
# 赋予类pos标签。
def pos_features(pos,feature_extraction_method):
	posFeatures = []
	for i in pos:
		posWords = [feature_extraction_method(i),'pos'] #为积极文本赋予"pos"
		posFeatures.append(posWords)
	return posFeatures

# 赋予类neg标签。
def neg_features(neg,feature_extraction_method):
	negFeatures = []
	for j in neg:
		negWords = [feature_extraction_method(j),'neg'] #为消极文本赋予"neg"
		negFeatures.append(negWords)
	return negFeatures

# Python 文本挖掘：使用机器学习方法进行情感分析（二、分割数据及赋予类标签）

def getwords(inputFile):
	f = open(inputFile, 'r',encoding='utf-8')
	words = []
	for line in f:
		ws = line.split()
		words.append([(w) for w in ws])
	f.close()
	return words

pos_review = getwords('datas/pos_feature.txt')
neg_review = getwords('datas/neg_feature.txt')


word_scores_1 = create_word_scores(pos_review,neg_review)
word_scores_2 = create_word_bigram_scores(pos_review,neg_review)
print(len(word_scores_1))
print(len(word_scores_2))
# for w in word_scores_1:
# 	print(w)
best_words1 = find_best_words(word_scores_1,8000)
best_words2 = find_best_words(word_scores_2,8000)
print(type(best_words1))
# for w in best_words1:
# 	print(w)


# 使用最好的特征值
pos = best_word_features(switch(pos_review),best_words1)
neg = best_word_features(switch(neg_review),best_words1)

posFeatures = pos_features(pos,bag_of_word)
negFeatures = neg_features(neg,bag_of_word)

shuffle(posFeatures) #把积极文本的排列随机化
shuffle(negFeatures)

print("pos length:"+str(len(posFeatures)))
print("neg length:"+str(len(negFeatures)))

poslen = len(posFeatures)
neglen = len(negFeatures)
size = poslen
if(size>neglen):
	size = neglen
posFeatures = posFeatures[:size]
negFeatures = negFeatures[:size]

trainRate = 0.8
trainIndex = int(size * trainRate) -1 
devIndex  = int(size * (trainRate + 0.1)) - 1
testIndex = size - 1 
# 使积极文本的数量和消极文本的数量一样。
# shuffle(pos_review) #把积极文本的排列随机化
# shuffle(neg_review)
# poslen = len(pos_review)
# neglen = len(neg_review)

# print("pos length:"+str(poslen))
# print("neg length:"+str(neglen))

# size = poslen
# if(size>neglen):
# 	size = neglen
# pos = pos_review[:size]
# neg = neg_review[:size]

# # 使用所有词（单词）作为特征
# posFeatures = pos_features(pos,bag_of_words)
# negFeatures = neg_features(neg,bag_of_words)

# 使用双词搭配作特征时的效果
# posFeatures = pos_features(pos,bigram)
# negFeatures = neg_features(neg,bigram)


# 使用所有词（单词）加上双词搭配作特征的效果
# posFeatures = pos_features(pos,bigram_words)
# negFeatures = neg_features(neg,bigram_words)

'''
# 计算信息量丰富的词，并以此作为分类特征
word_scores = create_word_scores()
best_words = find_best_words(word_scores, 1500) #选择信息量最丰富的1500个的特征

posFeatures = pos_features(best_word_features)
negFeatures = neg_features(best_word_features)

# 计算信息量丰富的词和双词搭配，并以此作为特征
word_scores = create_word_bigram_scores()
best_words = find_best_words(word_scores, 1500) #选择信息量最丰富的1500个的特征

posFeatures = pos_features(best_word_features)
negFeatures = neg_features(best_word_features)
'''

# for p in negFeatures:
# 	print(p)

# 把特征化之后的数据数据分割为开发集和测试集
# 这里把前124个数据作为测试集，中间50个数据作为开发测试集，最后剩下的大部分数据作为训练集。可以根据自己的需求修改


train = posFeatures[:trainIndex]+negFeatures[:trainIndex]
devtest = posFeatures[trainIndex:devIndex]+negFeatures[trainIndex:devIndex]
testset = posFeatures[devIndex:testIndex]+negFeatures[devIndex:testIndex]
# for t in train:
# 	print(t)

# Python 文本挖掘：使用机器学习方法进行情感分析（三、分类器及其准确度）
# 分割人工标注的标签和数据
dev, tag_dev = zip(*devtest) #把开发测试集（已经经过特征化和赋予标签了）分为数据和标签
test, tag_test = zip(*testset) #把测试集（已经经过特征化和赋予标签了）分为数据和标签
# for d in devtest:
# 	print(d)

# def build_model(features):	
# 	model = nltk.NaiveBayesClassifier.train(features)
# 	return model

# def probe_model(model,features,dataset_type='Train'):
# 	accuracy = nltk.classify.accuracy(model,features)
# 	print("\n"+dataset_type+"Accuracy = %0.2f"%(accuracy*100) + "%")

# def show_features(model,no_features=5):
# 	print("\nFeatures Importance")
# 	print('========================\n')
# 	print(model.show_most_informative_features(no_features))

# model = build_model(train)
# probe_model(model,train)
# probe_model(model,devtest,'Dev')
# show_features(model)

# 使用训练集训练分类器；
# 用分类器对开发测试集里面的数据进行分类，给出分类预测的标签；
# 对比分类标签和人工标注的差异，计算出准确度。
def score(classifier):
	classifier = SklearnClassifier(classifier) #在nltk 中使用scikit-learn 的接口
	classifier.train(train) #训练分类器

	# pred = classifier.batch_classify(testSet) #对开发测试集的数据进行分类，给出预测的标签
	pred = classifier.classify_many(dev)
	# return accuracy_score(tag_test, pred) #对比分类预测结果和人工标注的正确结果，给出分类器准确度
	return accuracy_score(tag_dev,pred)
	
print('BernoulliNB`s accuracy is %f' %score(BernoulliNB()))
print('MultinomiaNB`s accuracy is %f' %score(MultinomialNB()))
print('LogisticRegression`s accuracy is %f' %score(LogisticRegression()))
print('SVC`s accuracy is %f' %score(SVC()))
print('LinearSVC`s accuracy is %f' %score(LinearSVC()))
print('NuSVC`s accuracy is %f' %score(NuSVC()))

# 训练
BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(train)


test_review = getwords('datas/中国银行_split.txt')
p_file = open('datas/中国银行_socre.txt','w',encoding='utf-8') #把结果写入文档
for tr in test_review:
	testFeature = bag_of_words(tr)
	pred = BernoulliNB_classifier.prob_classify_many(testFeature) #该方法是计算分类概率值的
	content =" ".join(tr)
	for i in pred:
		p_file.write(content+","+str(i.prob('pos')) + ' ' + str(i.prob('neg')) + '\n')
p_file.close()

'''
dimension = ['500','1000','1500','2000','2500','3000']

for d in dimension:
	word_scores = create_word_bigram_scores()
	best_words = find_best_words(word_scores, int(d))

	posFeatures = pos_features(best_word_features)
	negFeatures = neg_features(best_word_features)


	train = posFeatures[174:]+negFeatures[174:]
	devtest = posFeatures[124:174]+negFeatures[124:174]
	test = posFeatures[:124]+negFeatures[:124]
	dev, tag_dev = zip(*devtest)

	print('Feature number %f' %d)
	print('BernoulliNB`s accuracy is %f' %score(BernoulliNB()))
	print('MultinomiaNB`s accuracy is %f' %score(MultinomialNB()))
	print('LogisticRegression`s accuracy is %f' %score(LogisticRegression()))
	print('SVC`s accuracy is %f' %score(SVC()))
	print('LinearSVC`s accuracy is %f' %score(LinearSVC()))
	print('NuSVC`s accuracy is %f' %score(NuSVC()))

# Python 文本挖掘：使用机器学习方法进行情感分析（四、使用分类器进行分类）  
word_scores = create_word_bigram_scores() #使用词和双词搭配作为特征
best_words = find_best_words(word_scores, 1500) #特征维度1500

posFeatures = pos_features(best_word_features)
negFeatures = neg_features(best_word_features)

trainSet = posFeatures[:500] + negFeatures[:500] #使用了更多数据
testSet = posFeatures[500:] + negFeatures[500:]
test, tag_test = zip(*testSet)

def final_score(classifier):
	classifier = SklearnClassifier(classifier)
	classifier.train(trainSet)
	pred = classifier.batch_classify(test)
	return accuracy_score(tag_test, pred)

print(final_score(BernoulliNB())) #使用开发集中得出的最佳分类器
'''

'''
# 把分类器存储下来
word_scores = create_word_bigram_scores()
best_words = find_best_words(word_scores, 1500)

posFeatures = pos_features(best_word_features)
negFeatures = neg_features(best_word_features)

trainSet = posFeatures + negFeatures

BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(trainSet)
pickle.dump(BernoulliNB_classifier, open('D:/code/sentiment_test/classifier.pkl','w'))
'''

'''
 # 把文本变为特征表示的形式
moto = pickle.load(open('D:/code/review_set/senti_review_pkl/moto_senti_seg.pkl','r')) #载入文本数据

def extract_features(data):
	feat = []
	for i in data:
		feat.append(best_word_features(i))
	return feat

moto_features = extract_features(moto) #把文本转化为特征表示的形式
clf = pickle.load(open('D:/code/sentiment_test/classifier.pkl')) #载入分类器

pred = clf.batch_prob_classify(moto_features) #该方法是计算分类概率值的
p_file = open('D:/code/sentiment_test/score/Motorala/moto_ml_socre.txt','w') #把结果写入文档
for i in pred:
	p_file.write(str(i.prob('pos')) + ' ' + str(i.prob('neg')) + '\n')
p_file.close()
'''