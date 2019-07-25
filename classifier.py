import sklearn
from feature_extraction import ArticleVector

#Following is somewhat unnecessary, but may be useful if we ever separate the data.
real_news_data = extract_urls('real_news_urls-training.txt')
real_news_data_X = [ArticleVector(url).vector for url in real_news_data]
real_news_data_Y = [1] * len(real_news_data_X)

fake_news_data = extract_urls('fake_news_urls-training.txt')
fake_news_data_X =  [ArticleVector(url).vector for url in fake_news_data]
fake_news_data_Y = [2] * len(fake_news_data_X)

opinion_data = extract_urls('opinion_urls-training.txt')
opinion_X = [ArticleVector(url).vector for url in opinion_data]
opinion_Y = [3] * len(opinion_X)

polarized_data = extract_urls('polarized_news_urls-training.txt')
polarized_X =  [ArticleVector(url).vector for url in polarized_data]
polarized_Y = [5] * len(polarized_X)

satire_data = extract_urls('satire_urls-training.txt')
satire_X =  [ArticleVector(url).vector for url in satire_data]
satire_Y = [7] * len(satire_X)

complete_X = real_news_data_X + fake_news_data_X + opinion_X + polarized_X + satire_X
complete_Y = real_news_data_Y + real_news_data_Y + opinion_Y + polarized_Y + satire_Y

def extract_urls(filename):
	'''
	takes a filename.txt with urls separated by spaces.
	'''
	file = open(filename, 'r')
	urls = file.read().split(' ')
	return urls

support_vector_machine = sklearn.svm.SVC(gamma = 'scale')
