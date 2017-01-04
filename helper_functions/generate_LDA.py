from __future__ import print_function
import re
import time
from collections import defaultdict
from random import shuffle
from shutil import rmtree as delete_dir

import numpy as np
from helper_functions.wordcloud_generator import *
from gensim import corpora, models
from nltk.stem import WordNetLemmatizer

from helper_functions.file import *

d = home
########################################################
final_lda_path = home + "FINAL_LDA/"
s = d + "data/"
LDA_savepath = d + "LDA_files/"
corpus_savepath = LDA_savepath + "Corpus/"
np.random.seed(42)

def LDA(texts, settings_list, score = True):
    """setings can be in list format or list of list if computing multiple iterations"""

    def create_corpus(transformation=None):
        # CREATING DICTIONARY
        wprint("Creating Word to Token Dictionary")
        dict_fname = "word2token.dict"
        dictionary = corpora.Dictionary(texts)
        dictionary.filter_extremes(no_below=5, no_above=0.5, keep_n=10000)
        dictionary.compactify()
        dictionary.save(corpus_savepath + dict_fname)

        if not score:
            dictionary.save(final_lda_path + dict_fname)

        # CREATING AND STORING VECTOR
        wprint("Creating Corpus")
        corpus = [dictionary.doc2bow(text) for text in texts]

        # RUNNING TRANSFORMATION
        if transformation == "tfidf":
            tfidf = models.TfidfModel(corpus)
            corpus = tfidf[corpus]

        corpora.MmCorpus.serialize(corpus_savepath + "main_corpus.mm", corpus)

        if not score:
            corpora.MmCorpus.serialize(final_lda_path + "main_corpus.mm", corpus)

        testing_corpus = []
        training_corpus = list(corpus)
        documents = range(0, len(corpus))
        wprint("Dividing training and test corpus")
        for i in range(0, len(corpus) / 3):  # divides corpus into approximately 1/3 testing and 2/3 training
            d = random.choice(documents)  # randomly selected document
            documents.remove(d)  # remove so it won't select the same document again
            testing_corpus.append(corpus[d])  # adds selected document to testing corpus
            training_corpus.remove(corpus[d])  # remove selected document from training corpus

        corpora.MmCorpus.serialize(corpus_savepath + "testing_corpus.mm", testing_corpus)
        corpora.MmCorpus.serialize(corpus_savepath + "training_corpus.mm", training_corpus)

    def create_lda_object(corpus_name, dict_name, settings):
        wprint("Loading Corpus")
        mm_corpus = corpora.MmCorpus(corpus_savepath + corpus_name)
        dictionary = corpora.Dictionary.load(corpus_savepath + dict_name)
        parameters = [ settings["num_topics"], settings["chunksize"],settings["passes"], settings["iterations"] ]
        wprint("Creating LDA Object with parameters " + str(parameters))

        lda = models.ldamodel.LdaModel(corpus=mm_corpus, id2word=dictionary, num_topics=settings["num_topics"],
                                       update_every=settings["update_every"], chunksize=settings["chunksize"],
                                       passes=settings["passes"], iterations=settings["iterations"], alpha='auto',
                                       minimum_probability=settings["minimum_probability"])
        return lda

    def record_perplexity(perplexity):
        line = ""
        for item in ["alpha", "num_topics", "chunksize", "passes", "iterations"]:
            line += item + ": " + str(settings[item]) + ", "

        l = []
        for item in ["num_topics", "chunksize", "passes" , "iterations"]:
            l.append(settings[item])
        line = line[:-2]  # take out last comma
        line = "log_p = " + str(perplexity) + '||Parameters: ' + " (" + str(l) + ")" + line

        pickle_file(line, "log_line")
        wprint("Perplexity determined: " + line)

    def score_lda(settings):
        testing_corpus = corpora.MmCorpus(corpus_savepath + "testing_corpus.mm")
        scoring_lda = create_lda_object("training_corpus.mm", "word2token.dict", settings)
        log_perplexity = scoring_lda.log_perplexity(testing_corpus)
        record_perplexity(log_perplexity)
        return scoring_lda, log_perplexity

    def log_runtime(string):
            p, i = unpickle("log_line").split("||")
            i = string + " / " + i
            log_writeline(p + " ||" + i)

    def wordcloud_format(topics):
        def generate_probability_str(wordtoprobdict):
            s = ""
            total_p = sum(wordtoprobdict.values())
            for word in wordtoprobdict:
                f = int(round(wordtoprobdict[word] / float(total_p) * 100))
                for i in range(0, f):
                    s += word + " "
            return s
        topic_to_words = defaultdict(lambda: defaultdict(str))
        topic_to_string = {}
        for topic in topics:
            t, words = int(topic[0]), topic[1]
            for word in words.split(" + "):
                p, word = word.split("*")
                p = float(p)
                topic_to_words[t][word] = p
            topic_string = generate_probability_str(topic_to_words[t])
            topic_to_string[t] = topic_string
        pickle_file(topic_to_string, "wordcloud", directory = settings["savepath"])

    def save_lda(lda):
        if not os.path.exists(settings["savepath"]):
            os.makedirs(settings["savepath"])
        lda.save(settings["savepath"] + 'Scoring_LDA')

    def check_save(lda, score):
        save = True
        top_50 = unpickle("top_50")
        lowest_score = top_50.keys()
        if len(lowest_score) == 0:
            save_lda(lda)
            return save
        lowest_score.sort()
        lowest_score = lowest_score[0]
        if score < lowest_score:
            save = False
        else:
            save_lda(lda)
            if len(top_50.keys()) >= 50:
                path = LDA_savepath + "LDA Objects/" + str(top_50[lowest_score])
                if os.path.exists(path):
                    delete_dir(path)
        return save
########################################################################################################################
    if type(settings_list) == dict:
        settings_list = [settings_list]
    create_corpus()

    total_runtime = 0
    number_of_runs, total_runs = 1, len(settings_list)
    for settings in settings_list:
        wprint("###############################################################################")
        wprint("RUNS: " + str(number_of_runs) + "/" + str(total_runs))
        wprint("###############################################################################")
        number_of_runs += 1

        ###########TIME_FUNCTION######################
        start = time.time()
        ##############################################
        if score:
            lda, score = score_lda(settings)
            topics = lda.show_topics(num_topics=10, num_words=40)
            sort_logging_lines()
            if check_save(lda,score):
                wordcloud_format(topics)
        else:
            print("Creating non-scoring LDA object")
            lda = create_lda_object("main_corpus.mm", "word2token.dict", settings)
            lda.save(final_lda_path + "FULL_LDA_" + settings["parameter_list"])
        ##############################################
        end = time.time()
        runtime = end - start
        total_runtime += runtime
        log_runtime("\tRuntime = " + str(runtime))
        wprint("Iteration Runtime: " + str(runtime))
        wprint("Total Runtime: " + str(round(total_runtime / 3600)) + ":" + str(round(total_runtime % 3600 / 60)))
        sort_logging_lines()
######################################################################33#########################

#SAVE FILE
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

# pickle_file(extract_texts("Abstract Compilation").read().split('/n'),"Abstract_Compilation_texts", directory=corpus_savepath)
# pickle_file(extract_texts(unpickle("abstract_list")), "miRNA_documents", directory = corpus_savepath)
##################################LOAD FILE######################################################
# texts = unpickle("Abstract_Compilation_texts", directory=corpus_savepath)
texts = unpickle("miRNA_documents", directory=corpus_savepath)
#################################################################################################
def run_LDA(settings_list = None, s = None, savepath = True, score = True):
    if not score:
        if not os.path.exists(final_lda_path):
            os.makedirs(final_lda_path)
    s_list = []
    if type(s) == list:
        settings_list = []
        settings_list.append(s)

    for parameters in settings_list:
        parameters = list(parameters)
        if savepath:
            e_savepath = LDA_savepath + "LDA Objects/" + str(parameters) + "/"
        else:
            e_savepath = savepath
        settings = {}
        settings["parameter_list"] = str(parameters)
        settings["savepath"] = e_savepath
        settings["transformation"] = None
        settings["update_every"] = 1
        settings["minimum_probability"] = 0.01
        settings["alpha"] = 'auto'
        settings["num_topics"], settings["chunksize"], settings["passes"], settings["iterations"] = parameters
        s_list.append(settings)
    shuffle(s_list)
    LDA(texts, s_list, score=score)
# run_LDA(s = [77,801,30,2500], score=False)
run_LDA(s = [5, 1600, 20, 2000], score = False)
def perform_experiment():
    settings_list = []
    for chunksize in range(1600, 3200, 800):
        for iterations in range(2000, 3000, 500):
            for passes in range(10,40,10):
                for num_topics in [5,10,15,20,57,90,125]:
                    settings_list.append((num_topics, chunksize, passes, iterations))
    run_LDA(settings_list=settings_list)
# perform_experiment()

def display_wordcloud(settings_list):
    e_savepath = LDA_savepath + str(settings_list) + "/"
    topic_to_string = unpickle("wordcloud", directory= e_savepath)
    for topic in topic_to_string.keys():
        fname = str("t#" + str(topic) + "-s" + str(settings_list))
        wordcloud(topic_to_string[topic], fname, show = False)


###################################TEST######################################################
# experiment(s= [100, 2000, 1, 2000])
# experiment(settings_list= [[100,1,1,2000],[400,250,1,1000],[100,200,1,3000]] )


# display_wordcloud([100,1,1,2000])

# string = "To assess the effects of ischemic preconditioning (IPC, 10-min ischemia/10-min reperfusion) on steatotic liver mitochondrial function after normothermic ischemia-reperfusion injury (IRI). METHODS: Sixty male Sprague-Dawley rats were fed 8-wk with either control chow or high-fat/high-sucrose diet inducing > 60% mixed steatosis. Three groups (n = 10/group) for each dietary state were tested: (1) the IRI group underwent 60 min partial hepatic ischemia and 4 h reperfusion; (2) the IPC group underwent IPC prior to same standard IRI; and (3) sham underwent the same surgery without IRI or IPC. Hepatic mitochondrial function was analyzed by oxygraphs. Mitochondrial Complex-I, Complex-II enzyme activity, serum alanine aminotransferase (ALT), and histological injury were measured. RESULTS: Steatotic-IRI livers had a greater increase in ALT (2476 +/- 166 vs 1457 +/- 103 IU/L, P < 0.01) and histological injury following IRI compared to the lean liver group. Steatotic-IRI demonstrated lower Complex-I activity at baseline [78.4 +/- 2.5 vs 116.4 +/- 6.0 nmol/(min.mg protein), P < 0.001] and following IRI [28.0 +/- 6.2 vs 104.3 +/- 12.6 nmol/(min.mg protein), P < 0.001]. Steatotic-IRI also demonstrated impaired Complex-I function post-IRI compared to the lean liver IRI group. Complex-II activity was unaffected by hepatic steatosis or IRI. Lean liver mitochondrial function was unchanged following IRI. IPC normalized ALT and histological injury in steatotic livers but had no effect on overall steatotic liver mitochondrial function or individual mitochondrial complex enzyme activities. CONCLUSION: Warm IRI impairs steatotic liver Complex-I activity and function. The protective effects of IPC in steatotic livers may not be mediated through mitochondria."
# wordcloud(string, "test", show= True)

#############################################SETTINGS########################################

# class gensim.models.ldamodel.LdaModel(corpus=None, num_topics=100, id2word=None, distributed=False, chunksize=2000, passes=1, update_every=1, alpha='symmetric', eta=None, decay=0.5, offset=1.0, eval_every=10, iterations=50, gamma_threshold=0.001, minimum_probability=0.01, random_state=None)

# #DEFAULT
# settings["num_topics"] = 100
# settings["update_every"] = 1
# settings["chunksize"] = 2000
# settings["passes"] = 1
# settings["iterations"] = 20000

# experiment(s=[95,501,6,501])