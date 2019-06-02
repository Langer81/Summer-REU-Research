'''
- Collect a lot of training data with indicators and predictors
- Identify important predictors 
- Create labeled training data along with test set let's say 75:25
- 
- Create the feature matrix and feed into SVM and create classifier

'''

'''
subtasks:
-figure out how to get a string from a url from article
'''
from sklearn.feature_extraction.text import TfidfVectorizer
import urllib.request
import bs4
import html2text
import requests
from goose3 import Goose

article_links = []
article_labels = []

def extract_urls():
	url_file = open('url_training_set.txt', 'r')
	lines = url_file.readlines()
	for i in range(len(lines)):
		lines[i] = lines[i][:len(lines[i]) - 1]
		splitted = lines[i].split(' ') #takes advantage of spaces being illegal in urls
		article_links.append(splitted[0])
		article_labels.append(splitted[1])


def file_to_string(filename):
	'''
	converts filename to a string
	returns string of all text in a file
	'''
	file = open(filename, 'r')
	text = file.read()
	file.close()
	return text

def url_to_goose_and_text(url):
	'''
	converts url to string
	returns goose3 object of article and full text of html page

	Possible problem: the returned string includes extra information from the whole page, rather than just the article itself.
	'''
	html = requests.get(url).text # string of htmls code
	text_maker = html2text.HTML2Text() 
	#define html options
	text_maker.ignore_links = True
	text_maker.skip_internal_links = True
	text_maker.IGNORE_IMAGES = True
	text_maker.IGNORE_TABLES = True
	text_maker.BYPASS_TABLES = True
	text_maker.ESCAPE_SNOB = True
	text = text_maker.handle(html)
	gooser = Goose()
	goosed_article = gooser.extract(url = url)
	return (goosed_article, text)

def Tfidf_predictors():
	'''
	returns tfidf sparse matrix of the article texts of all urls in article_links

	subtasks:
	1. identify which words will be the keys of the returned dictionary
	2. Later on parse the returned dictionary and form ints for as features for the matrix
	'''
	article_texts = []
	full_texts = [] # in case we need this in the future
	for url in article_links:
		parsed = url_to_goose_and_text(url)
		goose = parsed[0]
		full_text = parsed[1]
		cleaned_text = goose.title + ' ' +goose.cleaned_text
		article_texts.append(cleaned_text)
		full_texts.append(full_text)

	vectorizer = TfidfVectorizer()
	tfidf_sparse_matrix = vectorizer.fit_transform(article_texts)
	#tfidf_sparse_matrix = vectorizer.fit_transform(['and and and hello penis hello', 'hello hello and and','and and'])
	#print(article_texts)
	predictors = vectorizer.get_feature_names()
	print(len(vectorizer.vocabulary_))
	print(len(predictors))
	print(predictors)
	print('=--------')
	print(vectorizer.vocabulary_)
	return tfidf_sparse_matrix



def main():
	extract_urls()
	print(Tfidf_predictors())





if __name__ == "__main__": 
	main()

