from ap_style_checker import StyleChecker


def test_clean_word():
	word1 = 'Hi,'
	word2 = 'Hello:,'
	word3 = '!Greetings!,:[]('
	assert StyleChecker.clean_word(word1) == 'Hi', 'clean_word() test failed: expected: "Hi"  got:' + StyleChecker.clean_word(word1)
	assert StyleChecker.clean_word(word2) == 'Hello', 'clean_word() test failed: expected: "Hello"  got:' + StyleChecker.clean_word(word2)
	assert StyleChecker.clean_word(word3) == 'Greetings', 'clean_word() test failed: expected: "Greetings"  got:' + StyleChecker.clean_word(word3)
	print('... All clean_word() tests passed')

def test_numbers():
	test_sentence1 = StyleChecker('I ate one apple the other day.', 'Terrence Eats an Apple')
	test_sentence2 = StyleChecker('I ate 9 apple the other day.', 'Terrence Eats an Apple')
	test_sentence3 = StyleChecker('9 apples were eaten by Terrence that day.', 'Terrence Eats an Apple')
	test_sentence4 = StyleChecker('20 apples were eaten by Terrence that day.', 'Terrence Eats an Apple')
	assert test_sentence1.number_errors == 0, 'numbers() test failed: expected 0 got:' + str(test_sentence1.number_errors)
	assert test_sentence2.number_errors == 1, 'numbers() test failed: expected 1 got:' + str(test_sentence2.number_errors)
	assert test_sentence3.number_errors == 2, 'numbers() test failed: expected 2 got:' + str(test_sentence3.number_errors)
	assert test_sentence4.number_errors == 1, 'numbers() test failed: expected 1 got:' + str(test_sentence4.number_errors)
	print('... All numbers() tests passed')

def run_tests():
	test_clean_word()
	test_numbers()

run_tests()