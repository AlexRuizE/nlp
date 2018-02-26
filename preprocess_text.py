""" Functions to pre-process (cleaning html, tokenizing, tfidf, etc) text for higher-level NLP processing. """

import bs4
import re
import string
import math

class TextCleaner():
    """Clean text from html tags and punctuations, etc"""
    def clean_html(self, a_string):
        a_string = bs4.BeautifulSoup(a_string, "lxml").get_text()
        return a_string

    def clean_string(self, a_string):
        good_punctuation = re.compile('\'')
        punctuation = re.sub(good_punctuation, '', string.punctuation) + u"\u2018" + u"\u2019" + u"\u201D" + u"\u201C"  + u"\u2014" + u"\u2013"
        a_string = re.sub('-',' ', a_string)
        a_string = ''.join(char for char in a_string if char not in punctuation)
        a_string = a_string.lower()
        a_string = re.sub('\s{2,}',' ', a_string)
        a_string = re.sub('\'s','', a_string)
        a_string = a_string.split(' ')
        for element in a_string:
            if len(element) == 0: # 0 is empty string, 20 is to avoid urls and other garbage (30 is size longest english word in Oxford english dictionary)
                a_string.remove(element)
            elif len(element)>20:
                a_string.remove(element)
        a_string = ' '.join(a_string)
        a_string = re.sub('\n', ' ', a_string)
        return a_string

def tf(a_clean_string):
    """Create the TF part of TF-IDF. Tf will be index 0 of tuples within returned dictionary."""
    dict_per_doc = gen_dict(a_clean_string)
    a_clean_string = a_clean_string.split()
    done = []
    for word in a_clean_string:
        if word not in done:
            dict_per_doc[word] = dict_per_doc[word]+ (a_clean_string.count(word),)
            done.append(word)
    return dict_per_doc


def idf_denominator(corpus):
    # Corpus is a dict. IDF will be index 1 of tuples within returned dictionary.
    unique_words_global=dict()
    for document_key in list(corpus):
        document = clean_string(corpus[document_key])
        unique_words_doc = list(set(document.split()))
        for word in unique_words_doc:
            if word in unique_words_global:
                unique_words_global[word] += 1
            else:
                unique_words_global[word] = 1
    return unique_words_global

def gen_dict(a_clean_string):
    """ Populated with 2-tuple (tf, idf)"""
    d = dict()
    done = []
    a_clean_string = a_clean_string.split()
    for word in a_clean_string:
        if word not in done:
            d[word] = tuple()
            done.append(word)
    return d

def tfidf(corpus):
    """ Create TF-IDF values pero word/document. Returns dictionary of tuples (tf, idf, )"""
    N = len(corpus)
    docs_with_word = idf_denominator(corpus)
    global_dict = dict()
    for document_key in list(corpus):
        document = clean_string(corpus[document_key])
        if document_key in global_dict.keys():
            return print("Repeated key found:", document_key)
        else:
            global_dict[document_key] = tf(document)
    for document_key in global_dict:
        for term_key in global_dict[document_key]:
            document_count = docs_with_word[term_key]
            term_freq = global_dict[document_key][term_key][0]
            idf = math.log10(N/document_count)  # One possilbe flavor of TF-IDF.
            global_dict[document_key][term_key] += (round(idf, 3), round(term_freq * idf, 3))
    return global_dict

def all_words(a_clean_string):
    """Vocabulary size per string (e.g. a document)."""
    return set(a_clean_string)

def tokenize(a_clean_string, separator):
    """Tokenize a string. user can define its own token separator (e.g. ' '). """
    a_clean_string = list(a_clean_string.split(sep=separator))
    return a_clean_string

def is_noun(tag):
    """Boolean. Find nouns (Penn Treebank nomenclature)."""
    return tag in ['NN', 'NNS', 'NNP', 'NNPS']


def is_verb(tag):
    """Boolean. Find verbs (Penn Treebank nomenclature)."""
    return tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']


def is_adverb(tag):
    """Boolean. Find adverbs (Penn Treebank nomenclature)."""
    return tag in ['RB', 'RBR', 'RBS']


def is_adjective(tag):
    """Boolean. Find adjectives (Penn Treebank nomenclature)."""
    return tag in ['JJ', 'JJR', 'JJS']


def penn_to_wn(tag):
    """Convert Penn Treebank tagset to WordNet nomenclature for NLTK lemmatizer."""
    if is_adjective(tag):
        return wn.ADJ
    elif is_noun(tag):
        return wn.NOUN
    elif is_adverb(tag):
        return wn.ADV
    elif is_verb(tag):
        return wn.VERB
    return None

