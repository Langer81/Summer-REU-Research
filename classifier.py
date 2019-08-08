import sklearn
from feature_extraction import ArticleVector
import time
import numpy as np
import random

#Following is somewhat unnecessary, but may be useful if we ever separate the data.

#each filename should be a file containing article urls separated by spaces.
training_file_dict = {'real_news_urls-training.txt' : 1,'fake_news_urls-training.txt' : 2,'opinion_urls-training.txt' : 3,
					'polarized_news_urls-training.txt' : 5,'satire_urls-training.txt' : 7}
testing_file_dict = {'real_news_urls-testing.txt' : 1,'fake_news_urls-testing.txt' : 2,'opinion_urls-testing.txt' : 3,
					'polarized_news_urls-testing.txt' : 5,'satire_urls-testing.txt' : 7}

def extract_data(filename, label):
	data = extract_urls(filename)
	data_X = []
	count = 0
	for url in data[400: 800]:
		count += 1
		print('Current url:', url , '|| Visited', count, 'websites...')
		try:
			data_X.append(ArticleVector(url).vector)
		except:
			print('IT FAILED')
			continue
	data_Y = [label] * len(data_X)
	return data_X, data_Y #list of lists, list

def count_lines(filename):
	file = open(filename, 'r')
	lines = file.readlines()
	print(len(lines))

def write_feature_matrix_to_file(matrix, labels, write_file):
	### WILL NOT WORK WITH TWO DIGIT LABELS CARE CARE CARE
	'''
	matrix - list of lists
	labels - list of ints
	write_file - string
	'''
	file = open(write_file, 'a')
	assert len(matrix) == len(labels), 'len of list of feature matrices != len of list of labels'
	for i in range(len(matrix)):
		matrix[i].append(labels[i])
	for vector in matrix:
		file.write('\n')
		for element in vector:
			file.write(str(element) + ' ')
#write_feature_matrix_to_file([[1,2,3],[4,5,6],[7,8,9]], [67, 68, 69], 'testing69.txt')

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

		#time.sleep(sleep_time)
		xy_data = extract_data(filename, file_dict[filename])
		feature_matrices += xy_data[0]
		feature_labels += xy_data[1]

	return feature_matrices, feature_labels


#training_data = prepare_data(training_file_dict)
#testing_data = prepare_data(testing_file_dict)
#training_data_X = training_data[0]
#training_data_Y = training_data[1]
#testing_data_X = testing_data[0]
#testing_data_Y = testing_data[1]
#write_feature_matrix_to_file(training_data_X, training_data_Y, 'satire_vectors-testing.txt')

#count_lines('satire_vectors-testing.txt')

#support_vector_machine = sklearn.svm.SVC(gamma = 'scale')
#support_vector_machine.fit(complete_X, complete_Y)

def validate(model, X, Y):
	'''
	model - sklearn model with fit/predict
	X  - feature matrix i.e. list of lists
	Y  - corresponding y values 
	'''
	statistics_dict = {}
	predictions = []
	for vector in X:
		predictions.append(model.predict(np.array(vector).reshape(1, -1)))
	assert len(Y) == len(predictions), 'bruh the predictions and test_Y don\'t match in length'
	total = len(Y)
	correct = 0
	for i in range(len(predictions)):
		if predictions[i] == Y[i]:
			correct += 1
		else:
			statistics_dict[Y[i]] = statistics_dict.get(Y[i], 0) + 1
	percent_correct = (correct / total) * 100
	
	print(statistics_dict)
	print('This model got', str(percent_correct) + 'percent correct ||', str(correct), 'correct out of ', str(total))
	return percent_correct

def load_data(training_dict, cap = 0):
	'''
	training_dict: dictionary of string:int, where string is filename int is label
	cap = max number of data points we want to extract
	'''

	training_data = []
	labels = []
	for file in training_dict:
		current = open(file, 'r')
		data = current.readlines()
		limit = 0
		if cap == 0:
			limit = len(data)
		else:
			limit = cap
		print(limit)
		for i in range(limit):
			if len(data[i]) < 2:
				continue
			data[i] = data[i].strip().split(' ')
			
			
			assert type(data[i]) == list, 'not a list bruh'
			labels.append(data[i].pop(-1))
			training_data.append(data[i])
		current.close()
	#convert to int
	for i in range(len(training_data)):
		for j in range(len(training_data[i])):
			training_data[i][j] = float(training_data[i][j])
	return training_data, labels

training_file_dict = {'real_news_vectors-training.txt' : 1,'fake_news_vectors-training.txt' : 2,'opinion_vectors-training.txt' : 3,
					'polarized_news_vectors-training.txt' : 5,'satire_vectors-training.txt' : 7}
testing_file_dict = {'real_news_vectors-testing.txt' : 1,'fake_news_vectors-testing.txt' : 2,'opinion_vectors-testing.txt' : 3,
					'polarized_news_vectors-testing.txt' : 5,'satire_vectors-testing.txt' : 7}


def retrieve_data(file_dict, cap):
	'''
	returns:
	X: feature matrix from file dict
	'''

	print('Retreiving data...')
	training_data = load_data(file_dict, cap)
	X = training_data[0]
	Y = training_data[1]
	return X, Y

def svm_classifier(X_feature_matrix, Y_labels):
	support_vector_machine = sklearn.svm.SVC(gamma = 'scale')
	support_vector_machine.fit(X_feature_matrix, Y_labels)
	return support_vector_machine

def run_predictions(trained_classifier, test_X, test_Y):
	'''
	trained_classifier - a trained classifier from sklearn
	test_X - feature matrix for testing the classifier
	test_Y - list of labels that correspond to test_X
	'''
	predictions = []
	for vector in test_X:
		predictions.append(trained_classifier.predict(np.array(vector).reshape(1, -1)))
	return predictions

#validate(support_vector_machine, test_X, test_Y)

