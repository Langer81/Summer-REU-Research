from newspaper import Article
from goose3 import Goose

class ArticleVector:
	'''
	class whos purpose is to extract an article/urls vector for feature matrix
	'''
	reputable_news_sources = open('reputable_news_sources.txt', 'r').read().split(' ')
	def __init__(self, url):
		self.num_dimensions = 3 # changes as unique features are added
		self.url = url
		self.vector = [0] * self.num_dimensions 
		article = self.extract_article()
		self.title = article.title
		self.text = article.cleaned_text
		self.validate()
		self.fill_vector()

	def validate(self):
		if self.text == '':
			raise Exception('The text for this article is empty.')

	def extract_article(self):
		'''
		returns a goose article object
		'''
		gooser = Goose()
		article = gooser.extract(url = self.url)
		return article

	def url_ending_feature(self):
		'''
		returns 1 if url has reputable ending, 0 otherwise
		'''
		if '.com' in self.url or '.gov' in self.url or 'org' in self.url:
			return 1
		else:
			return 0
	def today_feature(self):
		'''
		returns the number of times "today" appears in the article text
		'''
		today_count = 0
		for word in self.text:
			if word == 'today' or word == 'Today':
				today_count += 1
		return today_count

	def from_reputable_source_feature(self):
		'''
		returns 1 if urls has reputable source in it
		'''
		for source in reputable_news_sources:
			if source in self.url:
				return 1
		return 0

	def fill_vector(self):
		'''
		calls all the methods created to fill in the articlevector
		'''
		self.vector[0] = self.url_ending_feature()
		self.vector[1] = self.from_reputable_source_feature()
		self.vector[2] = self.today_feature()