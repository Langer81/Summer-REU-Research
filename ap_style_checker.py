class StyleChecker:
	def __init__(self, text, title):
		self.title = title.split(' ')
		self.text_sentences = text.split('.')
		self.clean_list()
		self.total_errors = 0
		self.number_errors = 0
		self.scan()

	def clean_word(word):
		'''
		gets rid of punctation other than period
		'''

		exclude = set([',','/','!','?',';',':','"','[',']','(',')','|','-','_','*','&','^','%','#','@'])
		cleaned = ''.join([ch for ch in word if ch not in exclude])
		return cleaned

	def clean_list(self):
		'''
		removes any empty strings in the setnence list
		'''
		for i in range(len(self.text_sentences)):
			if self.text_sentences[i] == '':
				self.text_sentences.pop(i)

	def numbers(self, sentence):
		errors = 0
		word_list = sentence.split(' ')
		first_word = StyleChecker.clean_word(word_list[0])
		#print(word_list)
		def num_less_than_9(word):
			nonlocal errors
			try:
				num = int(word)
				if num <= 9:
					errors += 1
				return
			except:
				return
			

		def first_word_is_numeral(word):
			nonlocal errors
			try:
				num = int(word)
				if "year" not in word_list:
					errors += 1
				return
			except:
				return 
			 
		first_word_is_numeral(first_word)
		for word in word_list: #exclude the first word
			#print(word)
			cleaned_word = StyleChecker.clean_word(word) 
			num_less_than_9(cleaned_word)
		return errors
			


	def scan(self):
		for sentence in self.text_sentences:
			self.number_errors += self.numbers(sentence)

		self.total_errors = self.number_errors