def nth_index(string, char, n, index = 0):
	#return the index of the nth occurence of a character in a string
	if n == 0:
		return index - 1
	elif string == "":
		raise Exception('Substring not found bro')
	elif string[0] == char:
		return nth_index(string[1:], char, n - 1, index + 1)
	elif string[0] != char:
		return nth_index(string[1:], char, n, index + 1)

#print(nth_index('hello my name is terrence', 'h', 2))

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
			return word_contains(string1[1:], string2[1:])
		else:
			return word_contains(string1, string2[1:])
def test_word_contains():
	assert word_contains('wsj', 'wallstreetjournal') == True , 'bruh u wrong'
	assert word_contains('nytimes', 'thenewyorktimes') == True, 'bruh u wrong'
	assert word_contains('wsj', 'journalstreetwall') == False, 'bruh u wrong'
test_word_contains()