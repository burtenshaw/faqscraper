import imdb

import nlp
import corpus

from imdb._exceptions import IMDbDataAccessError, IMDbError

# Create the object that will be used to access the IMDb's database.
ia = imdb.IMDb()

# FAQs

# Split the Faqs into questions and answers return as list:

def faqSplitter(movie_id):

    try:
        faq = ia.get_movie_faqs(movie_id)['data']['faqs']
        x = []
        for i in faq:
            x.append(tuple(i.split('::')))
        return x
    except (RuntimeError, TypeError, NameError, KeyError, IOError, AssertionError, IMDbDataAccessError):
        pass

def faqScraper(index_file, output_file, start_from):

    faq_dict = corpus.load(start_from)
    f = corpus.load(index_file)
    print "Building Index"
    s = sorted(faq_dict.keys())
    x = []
    for i in f:
        if i[0] not in s:
            x.append(i[0])

    t = len(x)
    print str(t) + " ID's to scrape"

    if t < 1:
        pass
    else:
        print "Starting Scrape"
        for i in x:
            faq_dict.update(corpus.format(faqSplitter(i), i))
            t -= 1
            print(str(t) + ' To go')

        print('Saving')
        corpus.save(output_file, faq_dict)
    
index_file = "data/index_0.json"
output_file = "data/scraped.json"
start_from = "data/scraped.json"

faqScraper(index_file, output_file, start_from)

# for i in top250:
#     y = str(i)
#     x = faqSplitter(i)[2:]
#     faq_dict.update(corpus.format(x, y))

# corpus.save("data/top_250.json", faq_dict)