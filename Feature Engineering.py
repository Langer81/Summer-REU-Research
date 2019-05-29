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
def file_to_string(filename):
	'''
	converts filename to a string
	returns string of all text in a file
	'''
	file = open(filename, 'r')
	text = file.read()
	file.close()
	return text

def url_to_string(url):
	'''
	converts url to string
	returns string
	'''
	#text = urllib.request.urlopen(url).read()
	#type(text)
	html = requests.get(url).text # string of htmls code
	#text = soup.get_text()
	text = html2text.html2text(html)
	#text = html2text.html2text(text)
	#print('hello')
	return text

def frequency_predictor(url):
	'''
	text_article is a long string of the entire article
	return a dictionary of frequencies of different words

	subtasks:
	1. identify which words will be the keys of the returned dictionary
	2. Later on parse the returned dictionary and form ints for as features for the matrix
	'''
	
	vectorizer = TfidfVectorizer()
	predictors = vectorizer.fit_transform(text_article)

def main():
	print(url_to_string('https://empirenews.net/trump-works-out-deal-with-mexican-president-theyre-paying-for-the-wall-were-giving-them-back-texas/'))
if __name__ == "__main__": 
	main()

