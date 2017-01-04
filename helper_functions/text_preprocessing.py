from __future__ import print_function
from nltk.stem import WordNetLemmatizer
from helper_functions.file_handler import *

def extract_texts(documents):
    ########################PREPROCESSING#####################################
    class Thesaurus:
        def __init__(self):
            thesaurus = open(s + 'Thesaurus.txt').read().split("\n")
            synonym_to_word = {}
            for line in thesaurus:
                word = line.split("\t")[0]
                synonyms = line.split("\t")[1:]
                for synonym in synonyms:
                    synonym_to_word[synonym] = word
            self.words = synonym_to_word

        def stem(self, word):
            return self.words[word]
    class Stoplist:
        def __init__(self):
            self.words = set(open(d + "data/stopwords.txt").read().split("\n"))

        def add(self, word):
            if type(word) == list or type(word) == set:
                self.words.update(word)
            elif type(word) == str:
                self.words.add(word)

        def remove(self, word):
            if type(word) == list or type(word) == set:
                for w in word:
                    self.words.remove(w)
            elif type(word) == str:
                self.words.remove(word)
    stop = Stoplist()
    stop.add(
        ["significantly", "significant", "level", "effect", "increase", 'increased', "control", "chronic", "very",
         "result", "also"])
    stop.add(["one", "two", "three", "four", "five", "six", "seven", 'eight', "nine", "ten", "percent"])
    stop.add(["low", "high", "differ", "normal", "decrease", "used", "using", "uses"])
    stop.add(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'])
    def filter_stopwords(documents):
        """also deletes words of length less than 3"""
        texts = [[word for word in re.findall(r"[\w']+", document.lower().replace("'", "").replace('"', "")) if
                  word not in stop.words and len(word) > 2] for document in documents]
        return texts
    def filter_abstracts(abstract_list, min_length=100):
        """input list of abstracts in list of word form [[abstract], [abstract]]"""
        wprint("\tFiltering abstracts")
        keep_abstracts = []
        num_discarded = 0
        total_length = 0
        for abstract in abstract_list:
            length = len(abstract)
            total_length += length
            if length < min_length:
                num_discarded += 1
            else:
                keep_abstracts.append(tuple(abstract))
        wprint("\tNumber of abstracts discarded: " + str(num_discarded))
        wprint("\tAverage length of abstracts: " + str(total_length / float(len(abstract_list))))
        return keep_abstracts

    def stemming_text(texts):
        #STEMMING
        def stem_document(text_list):
            wnl = WordNetLemmatizer()
            t = []
            thesaurus = Thesaurus()
            for word in text_list:
                try:
                    t.append(thesaurus.stem(word))
                except:
                    t.append(wnl.lemmatize(word))
            return t
        wprint("Stemming Abstracts")
        stemmed_texts = []
        doc_number = 1
        total_docnum = len(texts)
        for doc in texts:
            print('\r\t%s out of %s' % (doc_number, total_docnum), end='')
            doc_number += 1
            stemmed_texts.append(stem_document(doc))
        texts = stemmed_texts
        # REFILTERING STOPWORDS
        texts = [[word for word in document if word not in stop.words] for document in texts]
        return texts
    ###########################################################################
    wprint("Extracting Documents")
    texts = filter_stopwords(documents)
    wprint("Begin preprocessing steps:")
    wprint("\tFiltering stopwords")
    return stemming_text(texts)