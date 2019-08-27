"# Summer-REU-Research" 
To the next PSU student who inherits this code:

The goal of this project is to create a multi-nomial classifier which takes an article url and labels it as either fake, real, satirical, polarized, opinion, misreporting, or persuasive information. (Each type is explained in the explication paper).

Important files:

feature_extraction.py - ArticleVector() will be your best friend this summer. ArticleVector will be how you vectorize an article into its respective features. You can find the features in the fill_vector() class:

classifier.py - This the initialization of the support vector machine. Basically the logistics of data preparation.

validator.py - this will help you validate the accuracy of your model. 

the .txt files are basically all for data collection. Their names should explain their respective uses. 


Features from the Explication paper that have been implemented:
1. Reputable URL ending (taken from "reputable_news_sources.txt") | boolean
2. whether or not a URL is from a reputable news source | boolean
3. number of times "Today" is written / total number of words | double
4. number of grammar mistakes | int
5. number of quotations / total number of words | double
6. number of past tense instances / total number of words | double 
7. number of present tense instances / total number of words | double
8. number of times "should" is written / total number of words | double
9. whether or not "opinion" is in the URL | boolean
10. number of words that are in all caps / total number of words | double
11. whether or not a URL is from a satire news source | boolean
12. number of apa errors | int
13. number of proper nouns that occur / total number of words | double
14. number of interjections that occur / total number of words | double
15. number of times "you" occcurs / total number of words | double
16. Whether a URL has a dot gov ending / total number of words | double
17. whether a URL is from an unreputable site (taken from "unreputable_news_sources.txt") | boolean

Important Features that have not been implemented:
1. Fact-checking news articles
2. Impartial reporting
3. Conflict
4. Human interest
5. Prominence 
6. Written by actual news staff
7. Clear About Us section
8. Emotionally charged words
9. Metadata
10. un/verified sources

These are the more signficant missing features. Basically, the current implemented features are the simpler, more trivial. The above features will require a lot more work.

Current classifier accuracy using support vector machine:
recall: [0.69642857 0.95535714 0.03125    0.30357143 0.89285714]
precision [0.82539683 0.87346939 0.5        0.24548736 0.50632911]
f1: [0.75544794 0.91257996 0.05882353 0.27145709 0.64620355]
{1: 68, 2: 10, 3: 217, 5: 156, 7: 24}
This model got 57.58928571428571 percent correct || 645 correct out of  1120

The indices of the recall/precision/f1 lists represent the labels of the type of news article:
0 = real news
1 = fake news
2 = opinion news
4 = polarized news
6 = satire data

As you can see, with the current 5 categories that have been implemented, there is a 58% accuracy, in the case that the base level without a classifier, and just tossing a coin is 20%
accurate. 

In order to use the classifier, first you must collect data. To do this use the prepare_data() method from classifier.py. The input is a dictionary with data text files as keys and their corresponding labels. see training_file_dict as an example. 

support_vector_machine = classifier.svm_classifier(train_X_uncombined, train_Y_uncombined)
svm_predictions = classifier.run_predictions(support_vector_machine, test_X_uncombined, test_Y_uncombined)
get_statistics(test_Y_uncombined, svm_predictions)
validate(support_vector_machine, test_X_uncombined, test_Y_uncombined)
^^these lines of code will be how you run the classifier for validation. 

***Important note***
data is separated out into urls, vectors, and then split into training and testing. There is no centralized collection of data. For example "Fake News" data will have 5 files:

1. fake_news_urls-testing.txt - text file with fake news urls separated by spaces for testing 
2. fake_news_urls-training.txt - text file with fake news urls separated by spacesA for training
3. fake_news_urls.txt - All fake news URLs compiled into one text file.
4. fake_news_vectors-testing.txt - The corresponding fake news testing URLs, from fake_news_urls-testing but vectorized into their respective features.
5. fake_news_vectors-training.txt - The corresponding fake news training URLs, from fake_news_urls-training but vectorized into their respective features.


More importantly, get in contact with me so I can explain everything much more accurately:

Cell: 814-308-4495
Email: terrencegl10@gmail.com

Good Luck.


