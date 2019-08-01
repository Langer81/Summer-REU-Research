from newspaper import Article
from goose3 import Goose
import language_check
import nltk
#from pyapa import pyapa
from ap_style_checker import StyleChecker

class ArticleVector:
	'''
	class whos purpose is to extract an article/urls vector for feature matrix
	'''
	NUM_DIMENSIONS = 18 # changes as unique features are added

	##### CLASS ATTRIBUTES #####

	reputable_news_sources = open('reputable_news_sources.txt', 'r').readlines()
	for i in range(len(reputable_news_sources)):
		reputable_news_sources[i] = reputable_news_sources[i].replace(" ", "").lower().strip()

	satire_news_sources = open('satire_news_sources.txt', 'r').readlines()
	for i in range(len(satire_news_sources)):
		satire_news_sources[i] = satire_news_sources[i].replace(" ", "").lower().strip()
	
	unreputable_news_sources = open('unreputable_news_sources.txt', 'r').readlines()
	for i in range(len(unreputable_news_sources)):
		unreputable_news_sources[i] = unreputable_news_sources[i].replace(" ", "").lower().strip()

	def word_contains(string1, string2):
		'''
		return true if string1 is inside string2 as long as the order fixed.
		ex: word_contains('wsj', 'wallstreetjournal')  -> True
		ex: word_contains('nytimes', 'thenewyorktimes') -> True
		ex: word_contains('wsj', 'journalstreetwall') -> False
		'''
		if string1 == '' and string2 != '':
			return True
		elif string1 != '' and string2 == '':
			return False
		elif string1 == '' and string2 == '':
			return True
		else:
			string1_first = string1[0]
			string2_first = string2[0]
			if string1_first == string2_first:
				return ArticleVector.word_contains(string1[1:], string2[1:])
			else:
				return ArticleVector.word_contains(string1, string2[1:])

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
			raise Exception('Substring not foundbro')
		elif string[0] == char:
			return ArticleVector.nth_index(string[1:], char, n - 1, index + 1)
		elif string[0] != char:
			return ArticleVector.nth_index(string[1:], char, n, index + 1)

	def num_periods_in_url(url):
		period_count = 0
		for letter in url:
			if letter == '.':
				period_count += 1
		return period_count
	##### INSTANCE ATTRIBUTES #####

	def __init__(self, url = "", text = ""):
		self.vector = [0] * ArticleVector.NUM_DIMENSIONS 
		self.url = url
		self.num_periods = ArticleVector.num_periods_in_url(self.url)
		self.cleaned_url = self.clean_url()
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

	def clean_url(self):
		'''
		ex: clean_url('https://www.nytimes.com/ijaw;efoija;wdlfkja;weifj') -> 'nytimes'
		'''
		if self.num_periods == 1:
			period_index = ArticleVector.nth_index(self.url, '.', 1)
			slash_index = ArticleVector.nth_index(self.url, '/', 2)
			return self.url[slash_index + 1 : period_index]
		elif self.num_periods == 2:
			first_period = ArticleVector.nth_index(self.url, '.', 1)
			second_period = ArticleVector.nth_index(self.url, '.', 2)
			return self.url[first_period + 1 : second_period]
		return ''
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

	

	def url_ending_index(self):
		'''
		returns 1 if url has reputable ending, 0 otherwise
		'''
		reputable_endings = ['.com', '.gov', '.org']
		if self.url == "":
			return None
		if self.num_periods == 1:
			period_index = ArticleVector.nth_index(self.url, '.', 1)
			ending = self.url[period_index : period_index + 4]
		elif self.num_periods == 2:
			period_index = ArticleVector.nth_index(self.url, '.', 2)
			ending = self.url[period_index : period_index + 4]
		else:
			return 0
		if ending in reputable_endings:
			return 1
		else:
			return 0

	def dot_gov_ending_index(self):
		if self.url == "":
			return None
		if self.num_periods == 1:
			period_index = ArticleVector.nth_index(self.url, '.', 1)
			ending = self.url[period_index : period_index + 4]
		elif self.num_periods == 2:
			period_index = ArticleVector.nth_index(self.url, '.', 2)
			ending = self.url[period_index : period_index + 4]
		else:
			return 0
		if ending == ".gov":
			return 1
		else:
			return 0
	'''
	def apa_index(self):
		
		returns number of apa errors
		
		checker = pyapa.ApaCheck()
		matches = checker.match(self.text)
		return len(matches)
	'''
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
		if 'opinion' in self.url or 'commentary' in self.url or 'editorial' in self.url:
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
			if source in self.cleaned_url:
				return 1
		return 0

	def all_caps_index(self):
		'''
		return the number of words in all caps in the title and body divided by the total number of words
		'''
		caps_index = 0
		for word in self.title.split(' '):
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
		for source in ArticleVector.satire_news_sources:
			if self.cleaned_url in source: # only different because satire is full link 
				return 1
		return 0

	def from_unreputable_source_index(self):
		for source in ArticleVector.unreputable_news_sources:
			#print(source)
			if source in self.url:
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

	def name_source_index(self):
		'''
		return the number of proper nouns in the text / total words
		'''
		num_prop_nouns = 0
		for pair in self.paired_tokens:
			if pair[1] == 'NNP':
				num_prop_nouns += 1
		return num_prop_nouns / self.num_words

	def interjection_index(self):
		'''
		return the number of interjections in the text / total words
		'''
		num_interjections = 0
		for pair in self.paired_tokens:
			if pair[1] == 'UH':
				num_interjections += 1
		return num_interjections / self.num_words

	def you_index(self):
		'''
		return the number of times "you" shows up in the text / total words
		'''
		num_yous = 0
		for word in self.text.split(' '):
			if word == 'you':
				num_yous += 1
		return num_yous / self.num_words

	def ap_style_index(self):

		checker = StyleChecker(self.text, self.title)
		return checker.total_errors

	def fill_vector(self):
		'''
		calls all the methods created to fill in self.vector
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
		#self.vector[12] = self.apa_index() # number of apa errors in an article
		self.vector[13] = self.name_source_index() # number of proper nouns in article / number of total words
		self.vector[14] = self.interjection_index() # number of interjections in article / number of total words
		self.vector[15] = self.you_index() # number of times you shows up in article / number of total words
		self.vector[16] = self.dot_gov_ending_index() # 1 if url ending is .gov, for persuasive information
		self.vector[17] = self.from_unreputable_source_index() # 1 if article is from unreputable source
		#self.vector[18] = self.ap_style_index() # number of ap style violations
