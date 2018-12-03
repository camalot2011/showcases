from pyspark import SparkContext, SparkConf
from lxml import html,etree
import sys
import os
from datetime import datetime
from myutils import Post, bool_to_int, add_two

def main(*args):
    if len(args) != 2:
        print("Please provide both input and output directories!")
        sys.exit(1)

    input_fn, output_fn = args[0], args[1]
    conf = SparkConf()
    conf.setAppName("Quickanswer")
    sc = SparkContext(conf=conf)

    posts = sc.textFile(input_fn)
    rdd_5 = (posts.map(lambda line: line.strip())
            .filter(lambda line: line.startswith('<row'))
            .filter(lambda line: '/>' in line)
            .map(Post.parse))
    
    joined_5 = (rdd_5.map(lambda x: (x.acceptedanswerid,(x.creationdate.year,
                                 x.creationdate.hour,x.creationdate)))
                 .join(rdd_5.map(lambda x: (x.Id,x.creationdate)))
                 .filter(lambda x: x[1][0][0]<2020)
                 .map(lambda x: (x[1][0][1],(x[1][1]-x[1][0][2]).total_seconds(),1))
                 .map(lambda x: (x[0],(bool_to_int(x[1]<3600*3),x[2])))
                 .reduceByKey(lambda x,y: add_two(x,y))
                 .map(lambda x: (x[0],x[1][0]/x[1][1]))
                 .sortByKey()
                 .saveAsTextFile(output_fn))
    
    
if __name__ == '__main__':
    main(*sys.argv[1:])
