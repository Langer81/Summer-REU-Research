from newspaper import Article
from goose3 import Goose

class ArticleVector:
	'''
	class whos purpose is to extract an article/urls vector for feature matrix
	'''
	reputable_news_sources = open('reputable_news_sources.txt', 'r').read().split(' ')
	def __init__(self, url):
		self.num_dimensions = 1
		self.url = url
		self.vector = [0] * self.num_dimensions # num_dimensions will increase as we add unique features
		article = self.extract_article()
		self.title = article.title
		self.text = article.cleaned_text

	def extract_article(self):
		'''
		returns a goose article object
		'''
		gooser = Goose()
		article = gooser.extract(url = self.url)
		return article

	def url_ending(self):
		'''
		returns 1 if url has reputable ending, 0 otherwise
		'''
		if '.com' in self.url or '.gov' in self.url or 'org' in self.url:
			return 1
		else:
			return 0

	def fill_article_vector(self):
		'''
		calls all the methods created to fill in the articlevector
		'''
		self.vector[0] = self.url_ending()