import classifier
import sklearn
from sklearn.metrics import recall_score, precision_score, f1_score, roc_auc_score
training_file_dict = {'real_news_vectors-training.txt' : 1,'fake_news_vectors-training.txt' : 2,'opinion_vectors-training.txt' : 3,
					'polarized_news_vectors-training.txt' : 5,'satire_vectors-training.txt' : 7}
testing_file_dict = {'real_news_vectors-testing.txt' : 1,'fake_news_vectors-testing.txt' : 2,'opinion_vectors-testing.txt' : 3,
					'polarized_news_vectors-testing.txt' : 5,'satire_vectors-testing.txt' : 7}

train_X, train_Y = classifier.retrieve_data(training_file_dict, 1000)
test_X, test_Y = classifier.retrieve_data(testing_file_dict, 225) 
true_Y = test_Y


###############################
####Support Vector Machine#####
###############################

def get_statistics(true_Y, predictions):
	results_dict = {}
	recall = recall_score(true_Y, predictions, average = None)
	precision = precision_score(true_Y, predictions, average = None)
	f1 = f1_score(true_Y, predictions, average = None)
	auc = roc_auc_score(true_Y, predictions)
	print('recall:', str(recall))
	print('precision', str(precision))
	print('f1:', str(f1))
	print('auc:', str(auc))
	return [recall, precision, f1, auc]

support_vector_machine = classifier.svm_classifier(train_X, train_Y)
svm_predictions = classifier.run_predictions(support_vector_machine, test_X, test_Y)
get_statistics(true_Y, svm_predictions)