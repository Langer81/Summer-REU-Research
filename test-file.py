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

print(nth_index('hello bitch my name is terrence', 'h', 2))