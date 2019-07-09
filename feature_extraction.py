from newspaper import Article
from goose3 import Goose
import language_check
import nltk

class ArticleVector:
	'''
	class whos purpose is to extract an article/urls vector for feature matrix
	'''
	reputable_news_sources = open('reputable_news_sources.txt', 'r').read().split(' ')
	num_dimensions = 6 # changes as unique features are added

	def __init__(self, url = "", text = ""):
		self.vector = [0] * ArticleVector.num_dimensions 
		self.url = url
		if text == "" and url != "": # user enters url
			article = self.extract_article()
			self.title = article.title
			self.text = article.cleaned_text
		elif text != "" and url == "": # user enters article text
			self.text = text
		self.paired_tokens = self.tokenize()
		self.validate()
		self.fill_vector()

	def validate(self):
		if self.text == '':
			raise Exception('The text for this article is empty.')
	
	def grammar_index(self):
		'''
		returns the number of grammar mistakes of the article divided by the length of the article
		

		checker = language_check.LanguageTool('en-US')
		matches = checker.check(self.text) # of typos. 
		return len(matches) / len(self.text)
		'''
		return 0
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
		return num_quotations

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
		return past_index

	def url_ending_index(self):
		'''
		returns 1 if url has reputable ending, 0 otherwise
		'''
		if self.url == "":
			return None
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
				return nth_index(string[1:], char, n - 1, index + 1)
			elif string[0] != char:
				return nth_index(string[1:], char, n, index + 1)

		reputable_endings = ['.com', '.gov', '.org']
		period_index = nth_index(self.url, '.', 2)
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
		for word in self.text:
			if word == 'today' or word == 'Today':
				today_count += 1
		return today_count

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