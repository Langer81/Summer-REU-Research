import newspaper
import xlrd
import xlwt
real_news_outlets = ['https://www.cnn.com', 
					'https://www.nytimes.com',
					 'https://www.wsj.com',
					 'https://www.usatoday.com',
					 'https://www.cbsnews.com',
					 'https://www.msn.com',
					 'https://www.npr.org',
					 'https://www.latimes.com',
					 'https://time.com/section',
					 'https://www.theguardian.com',
					 'https://www.washingtonpost.com',
					 'https://abcnews.go.com',
					 'https://news.yahoo.com',
					 'https://www.theatlantic.com',
					 'https://www.apnews.com',
					 'https://www.bbc.com',
					 'https://www.c-span.org',
					 'https://www.economist.com',
					 'https://www.propublica.org',
					 'https://www.reuters.com',
					 'https://www.pbs.org/newshour',
					 ]
opinion_news_outlets = ['https://www.wsj.com/news/opinion',
						'https://www.cnn.com/opinions'
						'https://www.nytimes.com/section/opinion',
						'https://www.usatoday.com/opinion',
						'https://www.latimes.com/opinion',
						'https://www.msn.com/en-us/news/opinion',
						'https://www.theguardian.com/us/commentisfree'
						'https://www.washingtonpost.com/opinions/'
						'https://time.com/tag/time-section-opinion/',
						'https://theweek.com/section/opinion',
						'https://www.newsweek.com/opinion',
						'https://nypost.com/opinion/',
						'https://www.newsday.com/opinion',
						'https://www.the-scientist.com/opinion'
						]
satire_news_outlets = ['http://www.hillarybeattrump.org',
						'https://aceflashman.wordpress.com',
						'https://adobochronicles.com',
						'https://babylonbee.com',
						'http://bigamericannews.com',
						'https://bluenewsnetwork.com',
						'https://www.theonion.com',
						'http://www.breakingburgh.com',
						'https://bullshitnews.org',
						'http://bizstandardnews.com',
						'https://www.burrardstreetjournal.com',
						'http://www.callthecops.net',
						'http://cap-news.com',
						'http://christwire.org',
						'http://civictribune.com',
						'https://www.clickhole.com',
						'https://confederacyofdrones.com',
						'https://www.cracked.com',
						'http://dailysnark.com',
						'https://www.dailysquib.co.uk',
						'https://dailyworldupdate.us',
						'http://www.derfmagazine.com',
						'http://duhprogressive.com',
						'https://empirenews.net',
						'https://empiresports.co',
						'https://encyclopediadramatica.rs/Main_Page',
						'https://www.enduringvision.com',
						'http://eveningharold.com',
						'http://www.eyeofthetiber.com',
						'https://www.flake.news',
						'http://fmobserver.com',
						'https://frankmag.ca',
						'https://freedumjunkshun.com',
						'https://gawken.com',
						'https://www.gishgallop.com',
						'https://gomerblog.com',
						'http://harddawn.com',
						'http://headlinennews.com',
						'https://www.huzlers.com',
						'https://chronicle.su',
						'http://ladiesofliberty.net',
						'http://www.larknews.com',
						'http://liberalbias.com',
						'http://liberaldarkness.com',
						'http://nationalreport.net',
						'https://www.newromantimes.com',
						]
polarized_news_outlets = ['http://allthatsfab.com/',
						'https://www.alternet.org/',
						'https://bluenationreview.com/',
						'https://bluestatedaily.com/',
						'https://www.breitbartunmasked.com/',
						'https://www.codepink.org/',
						'https://crooksandliars.com/',
						'https://www.dailydemocrat.com/',
						'https://www.dailykos.com/',
						'http://www.tribunemedia.com/tag/washington-dc/',
						'http://deepleftfield.info/',
						'https://democracyguardian.com/',
						'https://www.democraticunderground.com/',
						'https://egbertowillies.com/',
						'https://gopocalypse.net/',
						'https://republicanssuck.org/',
						'https://www.democratichub.com/',
						'https://washingtonpress.com/',
						'http://www.internationalviewpoint.org/',
						'https://www.2ndvote.com/',
						'https://abort73.com/',
						'https://www.aim.org/',
						'https://www.a1apac.org/',
						'https://aclj.org/',
						'https://www.axios.com/',
						'https://www.bizpacreview.com/',
						'https://www.christianheadlines.com/',
						'https://conservativebase.com/',
						'https://www.conservativedailynews.com/',
						'http://www.conservativehq.com/',
						'https://cowgernation.com/',
						'https://www.dailysignal.com/',
						'http://dcwhispers.com/',
						'http://federalistpress.com/',
						'https://www.dailywire.com/',
						'https://ussanews.com/News1/',
						]

def get_opinion_links():
	opinion_links = []
	for outlet in real_news_outlets:
		try:
			source = newspaper.build(outlet)
		except:
			continue
		categories = source.category_urls()
		for i in range(len(categories)):
			#print(categories[i])
			if ('opinion' in categories[i]):
				opinion_links.append(categories[i])
	return opinion_links




def feature_extraction(file):
	'''
	takes in a file of article urls and returns a 2d feature matrix.
	this should be the master methods with all the smaller feature methods called inside
	'''

	
#write_real_news_links_to_file(satire_news_outlets, 'satire_data.txt')

def write_to_file():
	write_news_links_to_file(real_news_outlets, 'real_news_data.txt')
	write_news_links_to_file(satire_news_outlets, 'satire_data.txt')

def read_fake_news_data_set(xl_file):
	'''
	meant to be used only for the excel sheet in the directory doesn't make sense otherwise
	'''
	file = xlrd.open_workbook(xl_file)
	sheet = file.sheet_by_name('fake')
	links = set()
	for i in range(0, 17949):
		val = str(sheet.cell(i, 8).value)
		if ' ' not in val and '.' in val:
			links.add(val)
	dirty_fake_news_outlets = list(links)
	for i in range(len(dirty_fake_news_outlets)):
		if 'http' not in dirty_fake_news_outlets[i]:
			dirty_fake_news_outlets[i] = 'https://www.' + dirty_fake_news_outlets[i]
	clean_fake_news_outlets = []
	for url in dirty_fake_news_outlets:
		if url in real_news_outlets or url in satire_news_outlets:
			continue
		clean_fake_news_outlets.append(url)
	write_news_links_to_file(clean_fake_news_outlets, 'fake_news_data.txt')
	
def create_training_and_test_sets(text_file):
	'''
	take a file like 'fake_news_urls.txt' and turn it into a training and test file 80 : 20
	'''
	training_ratio = 0.8
	print('hi')
	file = open(text_file, 'r')
	print(file)
	links = file.read().split(' ')
	#print(links)
	file.close()
	training_size = int(training_ratio * len(links))
	print(text_file[0 : len(text_file) - 4]  + "-training.txt")
	training_file = open(text_file[0 : len(text_file) - 4] + "-training.txt", 'w+')
	print(training_file)
	training_links = links[0 : training_size]
	testing_links = links[training_size : len(links)]
	for url in training_links:
		print(url)
		training_file.write(url + " ")
	training_file.close()
	testing_file = open(text_file[0 : len(text_file) - 4] + "-testing.txt", 'w+')
	for url in testing_links:
		print(url)
		testing_file.write(url + " ")
	testing_file.close()

#write_to_file()
#####################################################
#######Important functions: #########################
###############################################
def get_news_links(broad_news_outlet_url):
	article_links = []
	try:
		source = newspaper.build(broad_news_outlet_url)
	except:
		return []
	for article in source.articles:
		#if 'opinion' not in article.url and 'commentary' not in article.url:
		article_links.append(article.url)
	return article_links

def write_news_links_to_file(links_list, write_file):
	article_links = []
	for url in links_list:
		article_links.extend(get_news_links(url))
		print('getting', url , 'data ...')
	real_news_file  = open(write_file, 'w')
	for url in article_links:
		real_news_file.write(url + ' ')
	real_news_file.close()

def see_lengths(text_file):

	text_file = open(text_file, 'r')
	text = text_file.read().split(' ')
	print('number of article links:', len(text))


#see_lengths('opinion_data.txt')
#read_fake_news_data_set('fake_dataset.xlsx')
#get_opinion_article_links()
#opinion_links = get_opinion_links()
#write_news_links_to_file(opinion_news_outlets, 'opinion_data.txt') 
#write_news_links_to_file(polarized_news_outlets, 'polarized_news_urls')
#see_lengths('polarized_news_urls.txt')
#create_training_and_test_sets('polarized_news_urls.txt')
print(see_lengths('real_news_urls-training.txt'))