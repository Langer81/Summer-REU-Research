import newspaper
import xlrd
import xlwt
from feature_extraction import ArticleVector
real_news = open('reputable_news_sources.txt', 'r')
real_news_outlets = real_news.read().split(' ')
satire_news = open('satire_news_sources.txt', 'r')
satire_news_outlets = satire_news.read().split(' ')


def get_opinion_article_links():
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
	print(opinion_links)
	write_news_links_to_file(opinion_links, 'opinion_data.txt')

def get_news_links(broad_news_outlet_url):
	article_links = []
	try:
		source = newspaper.build(url)
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
	real_news_file  = open(write_file, 'w')
	for url in article_links:
		real_news_file.write(url + ' ')
	real_news_file.close()


def feature_extraction(file):
	'''
	takes in a file of article urls and returns a 2d feature matrix.
	this should be the master methods with all the smaller feature methods called inside
	'''

	
#write_real_news_links_to_file(satire_news_outlets, 'satire_data.txt')
def see_lengths():
	satire_file = open('satire_data.txt', 'r')
	satire = satire_file.read().split(' ')
	real_news_file = open('real_news_data.txt', 'r')
	real = real_news_file.read().split(' ')
	fake_news_file = open('fake_news_data.txt', 'r')
	fake = fake_news_file.read().split(' ')
	print('number of real news article links:', len(real))
	print('number of satire news article links:', len(satire))
	print('number of fake news article links:', len(fake))

def write_to_file():
	write_news_links_to_file(real_news_outlets, 'real_news_data.txt')
	write_news_links_to_file(satire_news_outlets, 'satire_data.txt')




####### One time uses #########
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

def remove_extras():
	file = open('satire_news_sources.txt', 'w')
	url_string = ''
	for url in satire_news_outlets:
		first_period = url.index('.')
		second_period = ArticleVector.nth_index(url, '.', 2)
		url_string += ' ' + url[first_period + 1 : second_period]
	file.write(url_string)

def get_urls():
	satire_file = open('satire_news_sources.txt', 'r')
	satire = satire_file.readlines()
	for i in range(len(satire)):
		try:
			first_paran = satire[i].index('(')
			second_paran = satire[i].index(')')
			satire[i] = satire[i][first_paran + 1 : second_paran]
		except:
			continue
	satire_file.close()
	file = open('satire_news_sources.txt','w')
	for source in satire:
		print(type(source))
		file.write(source + '\n')

#write_to_file()

#see_lengths()
#read_fake_news_data_set('fake_dataset.xlsx')
#get_opinion_article_links()
get_urls()