from newspaper import Article
from goose3 import Goose
import language_check
import nltk

class ArticleVector:
	'''
	class whos purpose is to extract an article/urls vector for feature matrix
	'''
	reputable_news_sources = open('reputable_news_sources.txt', 'r').read().split(' ')
	satire_news_sources = open('satire_news_sources.txt', 'r').read().split(' ')
	num_dimensions = 12 # changes as unique features are added

	def __init__(self, url = "", text = ""):
		self.vector = [0] * ArticleVector.num_dimensions 
		self.url = url
		if text == "" and url != "": # user enters url
			article = self.extract_article()
			self.title = article.title
			self.text = article.cleaned_text
		elif text != "" and url == "": # user enters article text
			self.text = text
		self.num_words = len(self.text.split(' '))
		self.paired_tokens = self.tokenize() #list of tuples ex. [('helped', 'VBD')]
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
		return len(matches) / self.num_words
		#return 0
	def extract_article(self):
		'''
		returns a goose article object
		'''

		gooser = Goose()
		article = gooser.extract(url = self.url)
		return article

	def quotation_index(self):
		num_quotations = 0
		for letter in self.text:
			if letter == '"':
				num_quotations += 1
		return num_quotations / self.num_words

	def tokenize(self):
		'''
		returns tokenized and classified versions of text using nltk
		'''
		tokens = nltk.word_tokenize(self.text)
		classified_tokens = nltk.pos_tag(tokens)
		return classified_tokens

	def past_tense_index(self):
		'''
		returns the number of past tense verbs in the text
		'''
		past_index = 0
		for pair in self.paired_tokens:
			if pair[1] == 'VBD' or pair[1] == 'VBN':
				past_index += 1
		return past_index / self.num_words

	def present_tense_index(self):
		'''
		returns the number of present tense verbs in the text over the 
		'''
		present_index = 0
		for pair in self.paired_tokens:
			if pair[1] == 'VBP' or pair[1] == 'VBZ' or pair[1] == 'VBG': # alter later if bad
				present_index += 1
		return present_index / self.num_words

	def nth_index(string, char, n, index = 0):
		'''
		return the index of the nth occurence of a character in a string
		string - string of interest
		char - char we're finding the index of 
		n - nth occurence of char
		index - index of char
		'''
		if n == 0:
			return index - 1
		elif string == "":
			raise Exception('Substring not found bro')
		elif string[0] == char:
			return ArticleVector.nth_index(string[1:], char, n - 1, index + 1)
		elif string[0] != char:
			return ArticleVector.nth_index(string[1:], char, n, index + 1)

	def url_ending_index(self):
		'''
		returns 1 if url has reputable ending, 0 otherwise
		'''
		if self.url == "":
			return None
		reputable_endings = ['.com', '.gov', '.org']
		period_index = ArticleVector.nth_index(self.url, '.', 2)
		ending = self.url[period_index : period_index + 4]
		if ending in reputable_endings:
			return 1
		else:
			return 0

	def today_index(self):
		'''
		returns the number of times "today" appears in the article text
		'''
		today_count = 0
		for word in self.text.split(' '):
			if 'today' in word or 'Today' in word:
				today_count += 1
		return today_count / self.num_words

	def should_index(self):
		'''
		returns the number of times "should" appears over the total number of words
		'''

		should_count = 0
		for word in self.text.split(' '):
			if 'should' in word or 'Should' in word:
				should_count += 1
		return should_count / self.num_words

	def opinion_index(self):
		'''
		returns 1 if 'opinion' or 'commentary' shows up in the url of an article
		'''
		if 'opinion' in self.url or 'commentary' in self.url:
			return 1
		else:
			return 0

	def from_reputable_source_index(self):
		'''
		returns 1 if urls has reputable source in it
		'''
		#print(ArticleVector.reputable_news_sources)
		for source in ArticleVector.reputable_news_sources:
			#print(source)
			if source in self.url:
				return 1
		return 0

	def all_caps_index(self):
		'''
		return the number of words in all caps in the title and body divided by the total number of words
		'''
		caps_index = 0
		for word in self.title:
			if word.isupper():
				caps_index += 1
		for word in self.text.split(' '):
			if word.isupper():
				caps_index += 1
		return caps_index / self.num_words

	def from_satire_source_index(self):
		'''
		returns 1 if link is from satire news source
		'''
		first_period_index = self.url.index('.')
		second_period_index = ArticleVector.nth_index(self.url, '.', 2)
		source = self.url[first_period_index + 1 : second_period_index]

		for outlet in ArticleVector.satire_news_sources:
			if outlet in source:
				return 1
		return 0

	def exclamation_index(self):
		'''
		returns number of exclamation points over total num of words.
		'''

		exclamation_index = 0
		for letter in self.text:
			if letter == '!':
				exclamation_index += 1
		return exclamation_index / self.num_words

	def fill_vector(self):
		'''
		calls all the methods created to fill in the articlevector
		'''
		self.vector[0] = self.url_ending_index() # reputable url ending feature 
		self.vector[1] = self.from_reputable_source_index() # reputable news source feature 
		self.vector[2] = self.today_index() #contains 'today' feature
		self.vector[3] = self.grammar_index() #number of grammar mistakes feature
		self.vector[4] = self.quotation_index() #number of times a "" shows up.
		self.vector[5] = self.past_tense_index() #number of times a past tense verb shows up
		self.vector[6] = self.present_tense_index() # number of times a present tense verb shows up / number of total words
		self.vector[7] = self.should_index() # number of times "should" shows up / number of total words
		self.vector[8] = self.opinion_index() # whether or not opinion shows up in url
		self.vector[9] = self.all_caps_index() # number of all caps words / number of total words
		self.vector[10] = self.from_satire_source_index() # whether article is from satire news outlet.
		self.vector[11] = self.exclamation_index() # number of exclamation points / number of total words