import sklearn
from feature_extraction import ArticleVector

#Following is somewhat unnecessary, but may be useful if we ever separate the data.
real_news_train_data = extract_urls('real_news_urls-training.txt')
real_news_train_data_X = [ArticleVector(url).vector for url in real_news_train_data]
real_news_train_data_Y = [1] * len(real_news_train_data_X)

real_news_test_data = extract_urls('real_news_urls-testing.txt')
real_news_test_data_X = [ArticleVector(url).vector for url in real_news_test_data]
real_news_test_data_Y = [1] * len(real_news_test_data_X)

fake_news_train_data = extract_urls('fake_news_urls-training.txt')
fake_news_train_data_X =  [ArticleVector(url).vector for url in fake_news_train_data]
fake_news_train_data_Y = [2] * len(fake_news_train_data_X)

fake_news_test_data = extract_urls('fake_news_urls-testing.txt')
fake_news_test_data_X =  [ArticleVector(url).vector for url in fake_news_test_data]
fake_news_test_data_Y = [2] * len(fake_news_data_test_X)

opinion_train_data = extract_urls('opinion_urls-training.txt')
opinion_train_X = [ArticleVector(url).vector for url in opinion_train_data]
opinion_train_Y = [3] * len(opinion_train_X)

opinion_test_data = extract_urls('opinion_urls-testing.txt')
opinion_test_X = [ArticleVector(url).vector for url in opinion_test_data]
opinion_test_Y = [3] * len(opinion_test_X)

polarized_train_data = extract_urls('polarized_news_urls-training.txt')
polarized_train_X =  [ArticleVector(url).vector for url in polarized_data]
polarized_train_Y = [5] * len(polarized_X)

polarized_test_data = extract_urls('polarized_news_urls-testing.txt')
polarized_test_X =  [ArticleVector(url).vector for url in polarized_test_data]
polarized_test_Y = [5] * len(polarized_test_X)

satire_train_data = extract_urls('satire_urls-training.txt')
satire_train_X =  [ArticleVector(url).vector for url in satire_train_data]
satire_train_Y = [7] * len(satire_train_X)

satire_test_data = extract_urls('satire_urls-testing.txt')
satire_test_X =  [ArticleVector(url).vector for url in satire_test_data]
satire_test_Y = [7] * len(satire_test_X)

complete_train_X = real_news_train_data_X + fake_news_train_data_X + opinion_train_X + polarized_train_X + satire_train_X
complete_train_Y = real_news_train_data_Y + fake_news_train_data_Y + opinion_train_Y + polarized_train_Y + satire_train_Y

complete_test_X = real_news_test_data_X + fake_news_test_data_X + opinion_test_X + polarized_test_X + satire_test_X
complete_test_Y = real_news_test_data_Y + fake_news_test_data_Y + opinion_test_Y + polarized_test_Y + satire_test_Y

def extract_urls(filename):
	'''
	takes a filename.txt with urls separated by spaces.
	'''
	file = open(filename, 'r')
	urls = file.read().split(' ')
	return urls

support_vector_machine = sklearn.svm.SVC(gamma = 'scale')
support_vector_machine.fit(complete_X, complete_Y)

def validate(model):
