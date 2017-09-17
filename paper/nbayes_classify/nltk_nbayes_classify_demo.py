import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews

def word_feats(words):
	return dict([(word, True) for word in words])

negids = movie_reviews.fileids('neg')
posids = movie_reviews.fileids('pos')
# print(type(negids))
# for n in negids[:10]:
# 	print(n)
# print(type(posids))
# for n in posids[:10]:
# 	print(n)

negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

# print(type(negfeats))
# print(type(posfeats))

negcutoff = int(len(negfeats)*3/4)
poscutoff = int(len(posfeats)*3/4)

trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]

for n in trainfeats[:2]:
	print(n)
print('+++++++++++++++++++++++++++++++++++++++++++++++')
for n in testfeats[:2]:
	print(n)

print('train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats)))
'''
classifier = NaiveBayesClassifier.train(trainfeats)
print('accuracy:', nltk.classify.util.accuracy(classifier, testfeats))
classifier.show_most_informative_features()
'''