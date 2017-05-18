import imdb
import check
import nlp
import corpus

from imdb._exceptions import IMDbDataAccessError, IMDbError

# Create the object that will be used to access the IMDb's database.
ia = imdb.IMDb()

# FAQs

# Split the Faqs into questions and answers return as list:
def faqSplitter(movie):
    try:
        ia.update(movie, 'faqs')
        faq = movie['faqs']
        x = []
        for i in faq:
            x.append(i.split('::'))
        return x
    except KeyError:
        pass


# print faqSplitter(film)

# Count the faqs
def faqCounter(movie):
    try:
        count = len(ia.get_movie_faqs(movie.movieID)['data']['faqs'])
        return count
    except KeyError:
        return 0

def faqTotalCount(movie_list):
    count = 0
    for i in movie_list:
        count += faqCounter(i)
    return count

def generalFaq(s_num, k_num):
    cnt = s_num
    x = []
    for i in range(1, k_num):
        cnt += 1
        movie_id = str(str(cnt).zfill(7))
        try:
            faq = len(ia.get_movie_faqs(movie_id)['data']['faqs'])
            if faq > 0:
                y = (movie_id, faq)
                x.append(y)
        except (RuntimeError, TypeError, NameError, KeyError, IOError, AssertionError, IMDbDataAccessError):
            pass
    return x

print "loading index"
k = corpus.load("data/index_0.json")
scrape = "data/scraped.json"
s_num = int(k[-1][0])

print "starting scrape loop"
for i in range(1,200):
    z = generalFaq(s_num, 1000)
    k.extend(z)
    f = "data/index_0.json"
    corpus.save(f, k)
    check.response(k, scrape)
    s_num += 1000
