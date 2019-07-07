from newspaper import Article
from goose3 import Goose
import language_check

class ArticleVector:
	'''
	class whos purpose is to extract an article/urls vector for feature matrix
	'''
	reputable_news_sources = open('reputable_news_sources.txt', 'r').read().split(' ')
	num_dimensions = 4 # changes as unique features are added

	def __init__(self, url):
		self.url = url
		self.vector = [0] * ArticleVector.num_dimensions 
		article = self.extract_article()
		self.title = article.title
		self.text = article.cleaned_text
		self.validate()
		self.fill_vector()

	def validate(self):
		if self.text == '':
			raise Exception('The text for this article is empty.')

	def grammar_index(self):
		'''
		returns the number of grammar mistakes of the article divided by the length of the article
		'''
	
		checker = language_check.LanguageTool('en-US')
		matches = checker.check(self.text) # of typos. 
		return len(matches) / len(self.text)

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
		reputable_endings = ['.com', '.gov', '.org']
		rear_period_index = self.url.rindex('.')
		ending = self.url[rear_period_index : rear_period_index + 4]

		if ending in reputable_endings:
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
		for source in ArticleVector.reputable_news_sources:
			if source in self.url:
				return 1
		return 0

	def fill_vector(self):
		'''
		calls all the methods created to fill in the articlevector
		'''
		self.vector[0] = self.url_ending_feature() # reputable url ending feature 
		self.vector[1] = self.from_reputable_source_feature() # reputable news source feature 
		self.vector[2] = self.today_feature() #contains 'today' feature
		self.vector[3] = self.grammar_index() #number of grammar mistakes feature