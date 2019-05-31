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
def file_to_string(filename):
	'''
	converts filename to a string
	returns string of all text in a file
	'''
	file = open(filename, 'r')
	text = file.read()
	file.close()
	return text

def url_to_goose(url):
	'''
	converts url to string
	returns goose3 object of article

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

def Tfidf_predictors(url):
	'''
	takes url of an article
	return tfidf features of the article

	subtasks:
	1. identify which words will be the keys of the returned dictionary
	2. Later on parse the returned dictionary and form ints for as features for the matrix
	'''
	parsed = url_to_goose(url)
	goose = parsed[0]
	full_text = parsed[1]
	cleaned_text = goose.cleaned_text
	vectorizer = TfidfVectorizer()
	X = vectorizer.fit_transform(cleaned_text.split())
	predictors = vectorizer.get_feature_names()
	return predictors
def main():
	print(Tfidf_predictors('https://www.cnn.com/business/live-news/stock-market-news-today-053119/h_44e0ad8e0780f08dd887f354c74ecb32'))
if __name__ == "__main__": 
	main()

