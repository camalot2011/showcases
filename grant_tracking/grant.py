from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql import functions as F
from pyspark.sql.types import *
from nltk.stem.porter import *
from pyspark.ml.feature import CountVectorizer, Tokenizer, IDF
from pyspark.ml.feature import StopWordsRemover
from pyspark.ml import Pipeline
from pyspark.ml.clustering import LDA
import numpy as np
import re
import sys
import os
from datetime import datetime
from myutils import text_cleaning, stem

def main(*args):
    if len(args) != 2:
        print("Please provide one input and one output directories!")
        sys.exit(1)

    input_fn, output_fn = args[0],args[1]
    conf = SparkConf()
    conf.setAppName("grant")
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    # Load the abstract content in the test folder into spark, 
    # clean text, tokenize the corpus, and stem the words
    abstract = sc.textFile(input_fn)
    df_abs = (abstract.map(lambda doc: text_cleaning(doc))
                      .filter(lambda doc: len(doc) > 0)
                      .filter(lambda line: not line.startswith('app'))
                      .map(lambda doc: doc.split(' '))
                      .map(lambda word: [x for x in word if len(x)>0])
                      .map(lambda word: stem(word))
                      .map(lambda doc: (int(doc[0]), doc[1:]))
                      .filter(lambda doc: len(doc[1])>0)
                      .toDF(['Id','words']))
    # build the pipeline and lda model with online optimizer
    stop_words = StopWordsRemover(inputCol='words',
                             outputCol='clean')
    stop_words.setStopWords(stop_words.loadDefaultStopWords('english'))
    countv = CountVectorizer(inputCol=stop_words.getOutputCol(), 
                             outputCol="tokens")
    idf = IDF(inputCol=countv.getOutputCol(),outputCol="features")
    lda = LDA(maxIter=10,k=10,optimizer='online')
    pipeline = Pipeline(stages=[stop_words, countv, idf, lda])
    lda_model = pipeline.fit(df_abs)
    labels = lda_model.transform(df_abs)
    
    # identify the label as the topic with the max probability
    # save the label to file
    topic_labels = (labels.select('Id','topicDistribution')
                          .rdd
                          .map(lambda x: (x[0],np.argmax(x[1])))
                          .saveAsTextFile(os.path.join(output_fn,'labels')))
    # Get the topics
    wordnum = 5 # choose the number of topic words
    vocabulary = lda_model.stages[1].vocabulary
    voc_bv = sc.broadcast(vocabulary)
    topic_df = (lda_model.stages[3].describeTopics(wordnum)
                     .rdd
                     .map(lambda x: (x[0],[voc_bv.value[Id] for Id in x[1]],x[2]))
                     .saveAsTextFile(os.path.join(output_fn,'words')))
    
if __name__ == '__main__':
    main(*sys.argv[1:])
