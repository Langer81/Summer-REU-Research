import sklearn
from feature_extraction import ArticleVector

#Following is somewhat unnecessary, but may be useful if we ever separate the data.

#each filename should be a file containing article urls separated by spaces.
training_file_dict = {'real_news_urls-training.txt' : 1,'fake_news_urls-training.txt' : 2,'opinion_urls-training.txt' : 3,
					'polarized_news_urls-training.txt' : 5,'satire_urls-training.txt' : 7}
testing_file_dict = {'real_news_urls-testing.txt' : 1,'fake_news_urls-testing.txt' : 2,'opinion_urls-testing.txt' : 3,
					'polarized_news_urls-testing.txt' : 5,'satire_urls-testing.txt' : 7}
testing69_dict = {'testing69.txt' : 69}
def extract_data(filename, label):
	data = extract_urls(filename)
	data_X = []
	for url in data:
		try:
			data_X.append(ArticleVector(url).vector)
		except:
			continue
	data_Y = [label] * len(data_X)
	return data_X, data_Y #list of lists, list


def write_feature_matrix_to_file(matrix, labels, write_file):
	'''
	matrix - list of lists
	labels - list of ints
	write_file - string
	'''

	file = open(write_file, 'w')
	assert len(matrix) == len(labels), 'len of list of feature matrices != len of list of labels'
	for i in range(len(matrix)):
		matrix[i].append(labels[i])
	for vector in matrix:
		for element in vector:
			file.write(str(element))
		file.write('\n')
write_feature_matrix_to_file([[1,2,3],[4,5,6],[7,8,9]], [67, 68, 69], 'testing69.txt')
def extract_urls(filename):
	'''
	takes a filename.txt with urls separated by spaces.
	'''
	file = open(filename, 'r')
	urls = file.read().split(' ')
	return urls

def prepare_data(file_dict):
	'''
	input : dictionary with string-filename keys, and int - label values
	returns : list of lists (x feature matrix), list of labels (ints)

	-basically returns complete_X and complete_Y
	'''
	
	feature_matrices = [] #List of feature vectors
	feature_labels = []
	for filename in file_dict:
		xy_data = extract_data(filename, file_dict[filename])
		feature_matrices += xy_data[0]
		feature_labels += xy_data[1]
	return feature_matrices, feature_labels

'''
training_data = prepare_data(training_file_dict)
testing_data = prepare_data(testing_file_dict)
training_data_X = training_data[0]
training_data_Y = training_data[1]
testing_data_X = testing_data[0]
testing_data_Y = testing_data[1]
write_feature_matrix_to_file(train)
'''


#support_vector_machine = sklearn.svm.SVC(gamma = 'scale')
#support_vector_machine.fit(complete_X, complete_Y)

def validate(model, X, Y):
	'''
	model - sklearn model with fit/predict
	X  - feature matrix i.e. list of lists
	Y  - corresponding y values 
	'''
	predictions = []
	for vector in X:
		predictions.append(model.predict(vector))
	assert len(Y) == len(predictions), 'bruh the predictions and test_Y don\'t match in length'
	total = len(Y)
	correct = 0
	for i in range(len(predictions)):
		if predictions[i] == Y[i]:
			correct += 1
	percent_correct = (correct / total) * 100
	print('This model got', str(percent_correct) + 'percent correct ||', str(correct), 'correct out of ', str(total))
	return percent_correct

