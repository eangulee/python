#nltk的贝叶斯分类器函数使用总结  
#先定义一个特征提取函数,该函数返回一个dict,其中key为维度名称,value为维度值  
def getFeature(sample):  
    return {'d1':5,'d2':False}  
  
#对每一个样本生成特征,然后将特征和样本的类别组成元组  
#样本元组 组成list类型的样本特征集  
train_set=[(getFeature(sample),class) for sample in samples]  
  
#使用train函数生成分类器:  
classifier=nltk.NaiveBayesClassifier.train(train_set)  
  
#使用测试集和nltk.classify.accuracy函数判断分类器的准确度  
print(nltk.classify.accuracy(classifier,test_set))
  
#使用分类器的classify函数判断某个实例的分类:  
classifier.classify(getFeature(Instance))  
  
#使用分类器的show_most_informative_features函数显示最有影响力的维度:  
classifier.show_most_informative_features(5)#显示头5个  