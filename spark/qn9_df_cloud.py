from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType
from pyspark.ml.feature import Word2Vec
from lxml import html,etree
import sys
import os
from datetime import datetime
from myutils import Post, localpath

def main(*args):
    if len(args) != 2:
        print("Please provide both input and output directories!")
        sys.exit(1)

    input_fn, output_fn = args[0], args[1]
    conf = SparkConf()
    conf.setAppName("Word2Vec")
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    # create the post table contains the tags info as a string
    posts = sc.textFile(input_fn)
    df_post = ((posts.map(lambda line: line.strip())
            .filter(lambda line: line.startswith('<row'))
            .filter(lambda line: '/>' in line)
            .map(Post.parse)
            .map(lambda x: (x.owneruserid,x.tags))
            .toDF(['ownerid','tags'])))
    # parse the tags using the generic functions into a list of words
    df_tags = (df_post.withColumn('input',F.regexp_replace(F.col('tags'),'<',''))
                  .withColumn('input',F.lower(F.col('input')))
                  .withColumn('input',F.split(F.col('input'),'>')))
    # build the machine learning pipeline
    w2v = Word2Vec(inputCol="input", outputCol="vectors", 
                   vectorSize=100, minCount=10, seed=42)
    model = w2v.fit(df_tags)
    result = model.transform(df_tags)
    (model.findSynonyms("ggplot2", 25)
          .rdd
          .map(lambda x: (x[0],x[1]))
          .saveAsTextFile(output_fn))
    
    
    
if __name__ == '__main__':
    main(*sys.argv[1:])
