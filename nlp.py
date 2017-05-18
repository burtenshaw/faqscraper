from nltk import word_tokenize
import nltk
from nltk.tag import pos_tag

def posScraper(string, X):
    text = nltk.pos_tag(word_tokenize(string))
    pos = []
    for i in text:
        if i[1].startswith(X):
            pos.append(i[0])
    return pos

def sieve(string_list):
    string_list.sort(key=lambda s: len(s), reverse=True)
    out = []
    for s in string_list:
        if not any([s in o for o in out]):
            out.append(s)
    return out

def bagger(string_list, X):
    string_list = sieve(string_list)
    bag = []
    for i in string_list:
        for x in posScraper(i, X):
            if x not in bag:
                bag.append(x)
    return bag

def crossBagger(X,Y):
    words = []
    for i in X:
        if i in Y:
            words.append(i)
    words = sieve(words)
    return words


def phraseScraper(string, pos_list, window):
    list = string.split()
    pos_phrases = []
    for i,item in enumerate(list):
        if item in pos_list:
            phrase = list[i-window], list[i], list[i+window]
            pos_phrases.append(phrase)
    return pos_phrases

def phraseMaker(string, pos_list):
    list = string.split()
    print(list)
    phrases = []
    for i,item in enumerate(list):
        if i <= 1:
            continue
        if item not in pos_list:
            continue
        elif item in pos_list:
            if item in phrases[i-1]:
                phrases[i-1] = " ".join(list[i])
            else:
                phrases = phrases.append(list[i])

        phrases.append(phrase)
    return phrases

def nounPhrases(string):
    grammar = r"""
        NP: {<DT|PP\$>?<JJ>*<NN>}   # chunk determiner/possessive, adjectives and noun
        {<NNP>+}                # chunk sequences of proper nouns
        {<NN>+}                 # chunk consecutive nouns
        """

    cp = nltk.RegexpParser(grammar)
    tagged_sent = nltk.pos_tag(string.split())
    parsed_sent = cp.parse(tagged_sent)
    for subtree in parsed_sent.subtrees():
      if subtree.label() == 'NP':
        yield ' '.join(word for word, tag in subtree.leaves())

def nounPropper(string):
    grammar = r"""
        NNP: {<DT|PP\$>?<JJ>*<NNP>}
        {<NNP>+}                # chunk sequences of proper nouns
        """
    cp = nltk.RegexpParser(grammar)
    tagged_sent = nltk.pos_tag(string.split())
    parsed_sent = cp.parse(tagged_sent)
    for subtree in parsed_sent.subtrees():
      if subtree.label() == 'NNP':
        yield ' '.join(word for word, tag in subtree.leaves())


## to use nounPhrases
# for npstr in nounPhrases(string):
#     print npstr

def propperNounList(string):
    # takes in a plain string and gives back a list of the propper nouns.
    sent_tokenized = word_tokenize(string)
    pn_list = []
    for npstr in nounPropper(string):
         pn_list.append(npstr)
    return pn_list

def questionMaker(data):
    questions_answers = []
    with open(data) as file:
        for i in file:
            if "?" in i:
                pair = []
                pair.append(i)
                pair.append(next(file))
                questions_answers.append(tuple(pair))
    return questions_answers

def questionList(list):
    questions_answers = []
    for i in list:
        if "?" in i:
            pair = []
            pair.append(i)
            pair.append(i + 1)
            questions_answers.append(tuple(pair))
    return questions_answers

# Make paragraphs into sentences

def sentence_tokenizer(string):
    import nltk.data
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sentence_list = sent_detector.tokenize(string.strip())
    return sentence_list
