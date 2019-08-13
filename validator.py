import classifier
import sklearn
from sklearn.metrics import recall_score, precision_score, f1_score, roc_auc_score
import numpy as np

training_file_dict = {'real_news_vectors-training.txt' : 1,'fake_news_vectors-training.txt' : 2,'opinion_vectors-training.txt' : 3,
					'polarized_news_vectors-training.txt' : 5,'satire_vectors-training.txt' : 7}
testing_file_dict = {'real_news_vectors-testing.txt' : 1,'fake_news_vectors-testing.txt' : 2,'opinion_vectors-testing.txt' : 3,
					'polarized_news_vectors-testing.txt' : 5,'satire_vectors-testing.txt' : 7}

train_X, train_Y = classifier.retrieve_data(training_file_dict, 1000)
test_X, test_Y = classifier.retrieve_data(testing_file_dict, 225) 
true_Y = test_Y

def validate(model, X, Y):
	'''
	model - sklearn model with fit/predict
	X  - feature matrix i.e. list of lists
	Y  - corresponding y values 
	'''
	statistics_dict = {}
	predictions = []
	for vector in X:
		predictions.extend(model.predict(np.array(vector).reshape(1, -1)))
	assert len(Y) == len(predictions), 'bruh the predictions and test_Y don\'t match in length'
	total = len(Y)
	#print(predictions)
	correct = 0
	for i in range(len(predictions)):
		#print(Y[i] == predictions[i])
		#print(float(predictions[i]))
		#print(Y[i])

		if float(predictions[i]) == float(Y[i]):
			correct += 1
		else:
			statistics_dict[Y[i]] = statistics_dict.get(Y[i], 0) + 1
	percent_correct = (correct / total) * 100
	
	print(statistics_dict)
	print('This model got', str(percent_correct) + 'percent correct ||', str(correct), 'correct out of ', str(total))
	return percent_correct

def get_statistics(true_Y, predictions):
	results_dict = {}
	recall = recall_score(true_Y, predictions, average = None)
	precision = precision_score(true_Y, predictions, average = None)
	f1 = f1_score(true_Y, predictions, average = None)
	#auc = roc_auc_score(true_Y, predictions, average = 'micro')
	print('recall:', str(recall))
	print('precision', str(precision))
	print('f1:', str(f1))
	#print('auc:', str(auc))
	return [recall, precision, f1]

###############################
####Support Vector Machine#####
###############################
support_vector_machine = classifier.svm_classifier(train_X, train_Y)
svm_predictions = classifier.run_predictions(support_vector_machine, test_X, test_Y)
get_statistics(true_Y, svm_predictions)
validate(support_vector_machine, test_X, true_Y)

def find_errors(model, vector_data_file, label):
	'''
	returns a dictionary that tells you how many of each category the model incorrectly predicted. 
	IT TELLS NUMBER OF INCORRECT, NOT CORRECT
	'''
	data, labels = classifier.load_data({vector_data_file : label}, cap = 225)
	incorrect_predictions = {}
	model_predictions =[]
	for vector in data:
		model_predictions.extend(model.predict(np.array(vector).reshape(1, -1)))
	#print(model_predictions[0])
	#print(model_predictions)
	for i in range(len(model_predictions)):
		if float(model_predictions[i]) != float(label):
			#print(str(model_predictions[i]), str(label))
			incorrect_predictions[model_predictions[i]] = incorrect_predictions.get(model_predictions[i], 0) + 1
	
	print(incorrect_predictions)
	return incorrect_predictions
def vector_diagnostics(vector_data_file, label):
	data, labels = svm_classifier.load_data({vector_data_file : label})
# print('False negatives for Opinion data:')
# find_errors(support_vector_machine, 'opinion_vectors-testing.txt', 3)
# print('False negatives for Polarized News data:')
# find_errors(support_vector_machine, 'polarized_news_vectors-testing.txt', 5)
for file in testing_file_dict:
	title = file[:file.index('_')]
	print('False negatives for', title, 'data (' + str(testing_file_dict[file]) + ')')
	find_errors(support_vector_machine, file, testing_file_dict[file])
