import sklearn
from feature_extraction import ArticleVector
training_files = ['real_news_urls.txt', 'satire_urls.txt', 'fake_news_urls.txt']



def prepare_data():
	training_urls = []
	feature_matrix = []
	label_vector = []
	for file in training_files:
		open_file = open(file, 'r')
		training_urls.extend(open_file.read().split(' '))
	for url in training_urls:
		label = training_files.index(file.name) # label is the index of the file name in training_files
		label_vector.append(label)
		article = ArticleVector(url = url)
		feature_matrix.append(article.vector)
	return feature_matrix, label_vector

