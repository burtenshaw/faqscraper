import imdb

import nlp
import corpus

# Create the object that will be used to access the IMDb's database.
ia = imdb.IMDb()

def indexFaqCounter(k):
	cnt = 0
	for i in k:
		cnt += i[1]
	current_id = k[-1][0]
	print "Latest Movie ID: " + str(current_id)
	highest_id = 6799992
	percent = 100 * float(current_id)/float(highest_id)
	print "\n Indexed"
	print "________"
	print "Percentage: " + str(float("{0:.2f}".format(percent))) + "%"
	print "Total faqs found: " + str(cnt)
	print "Total Films indexed: " + str(len(k))

def scrapeFaqChecker(k):
	cnt = 0
	for key, value in k.iteritems():
		try:
			cnt += len(value)
		except TypeError:
			pass

	print "Total faqs scraped: " + str(cnt)
	print "Total films scraped: " + str(len(k))


infex_file = corpus.load("data/index_0.json")
indexFaqCounter(infex_file)