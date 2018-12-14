from datetime import datetime
from nltk.stem.porter import *
from pyspark.sql import functions as F
from pyspark.sql.types import *
import os
import re

def text_cleaning(doc):
    '''lower case, clean words/symbols'''
    rm_list ='\"|\,|\(|  +|\)|\.|\'|\:'
    doc = re.sub(r'{}'.format(rm_list),' ',doc)
    doc = doc.strip().lower()
    return doc

def stem(words):
    '''Get the stem of the words'''
    stemmer = PorterStemmer()
    words_stem = []
    for word in words:
        word_stem = stemmer.stem(word)
        if len(word_stem) > 2:
            words_stem.append(word_stem)
    return words_stem
