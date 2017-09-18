from nltk.corpus import movie_reviews
from sklearn.cross_validation import StratifiedShuffleSplit
import nltk
from nltk.corpus import stopwords
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

# 获取数据
def get_data():
	dateset = []
	y_lables = []
	for cat in movie_reviews.categories():
		# print('cat:'+cat)
		for fileid in movie_reviews.fileids(cat):
			# print('fileid:'+fileid)
			words = list(movie_reviews.words(fileid))
			# wordstr = ''
			# for w in words:
			# 	wordstr += w +' '
			# print(wordstr)
			dateset.append((words,cat))
			y_lables.append(cat)
	return dateset,y_lables

# 获取训练和测试集
def get_train_test(input_dataset,y_lables):
	train_size = 0.7
	test_size = 1 - train_size
	stratified_split = StratifiedShuffleSplit(y_lables,test_size=test_size,n_iter=1,random_state=77)
	for train_index,test_index in stratified_split:
		train = [input_dataset[i] for i in train_index]
		train_y = [y_lables[i] for i in train_index]	

		test = [input_dataset[i] for i in test_index]
		test_y = [y_lables[i] for i in test_index]	 
	return train,test,train_y,test_y

def build_word_features(instance):
	feature_set = {}
	words = instance[0]
	for word in words:
		feature_set[word] = 1	
	return (feature_set,instance[1])

def build_negate_features(instance):
	words = instance[0]
	final_words = []
	negate = False
	negate_words = ['no','not']
	for word in words:
		if negate:
			word = "Not_" + word
			negate = False
		if word not in negate_words:
			final_words.append(word)
		else:
			negate = True
	feature_set = {}
	for word in final_words:
		feature_set[word] = 1
	return (feature_set,instance[1])

def remove_stop_words(in_data):
	stopword_list = stopwords.words('english')
	negate_words = ['no','not']
	new_stopwords = [word for word in stopword_list if word not in negate_words]
	label = in_data[1]
	words = [word for word in in_data[0] if word not in negate_words]
	return (words,label)

def build_keyphrase_features(instance):
	feature_set = {}
	instance = remove_stop_words(instance)
	words = instance[0]
	bigram_finder = BigramCollocationFinder.from_words(words)
	bigrams = bigram_finder.nbest(BigramAssocMeasures.raw_freq,400)
	for bigram in bigrams:
		feature_set[bigram] = 1
	return (feature_set,instance[1])

def build_model(features):	
	model = nltk.NaiveBayesClassifier.train(features)
	return model

def probe_model(model,features,dataset_type='Train'):
	accuracy = nltk.classify.accuracy(model,features)
	print("\n"+dataset_type+"Accuracy = %0.2f"%(accuracy*100) + "%")

def show_features(model,no_features=5):
	print("\nFeatures Importance")
	print('========================\n')
	print(model.show_most_informative_features(no_features))	
	
def build_model_cycle_1(train_data,dev_data):
	train_features = map(build_word_features,train_data)
	# print(type(train_features))
	# for t in train_features:
	# 	print(t)
	dev_features = map(build_word_features,dev_data)
	model = build_model(train_features)

	probe_model(model,train_features)
	probe_model(model,dev_features,'Dev')

	return model

def build_model_cycle_2(train_data,dev_data):
	train_features = map(build_negate_features,train_data)
	dev_features = map(build_negate_features,dev_data)

	model = build_model(train_features)

	probe_model(model,train_features)
	probe_model(model,dev_features,'Dev')

	return model

def build_model_cycle_3(train_data,dev_data,test_data):
	train_features = map(build_keyphrase_features,train_data)
	dev_features = map(build_keyphrase_features,dev_data)

	model = build_model(train_features)

	probe_model(model,train_features)
	probe_model(model,dev_features,'Dev')
	test_features = map(build_keyphrase_features,test_data)
	probe_model(model,test_features,'Test')

	return model

if __name__ == "__main__":
	input_dataset,y_lables = get_data()
	train_data,all_test_data,train_y,all_test_y = get_train_test(input_dataset,y_lables)
	dev_data,test_data,dev_y,test_y = get_train_test(all_test_data,all_test_y)
	print("\nOriginal Data Size:"+str(len(input_dataset)))
	print("\nTraining Data Size:"+str(len(train_data)))
	print("\nDev Data Size:"+str(len(dev_data)))
	print("\nTesting Data Size:"+str(len(test_data)))


	model_cycle_1 = build_model_cycle_1(train_data,dev_data)
	show_features(model_cycle_1)

	model_cycle_2 = build_model_cycle_2(train_data,dev_data)
	show_features(model_cycle_2)

	model_cycle_3 = build_model_cycle_3(train_data,dev_data,test_data)
	show_features(model_cycle_3)