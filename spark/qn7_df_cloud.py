from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType,IntegerType
from pyspark.sql.window import Window
from lxml import html,etree
import sys
import os
from datetime import datetime
from myutils import Post, User, localpath

def main(*args):
    if len(args) != 4:
        print("Please provide two input and two output directories!")
        sys.exit(1)

    input_fn_user, input_fn_post = args[0],args[1]
    output_fn_vet, output_fn_brief = args[2], args[3]
    conf = SparkConf()
    conf.setAppName("Veterans")
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    
    users = sc.textFile(input_fn_user)
    df_user = ((users.map(lambda line: line.strip())
            .filter(lambda line: line.startswith('<row'))
            .filter(lambda line: '/>' in line)
            .map(User.parse)
            .map(lambda x: (x.Id,x.creationdate))
            .toDF(['userid','usercreationdate'])))
    
    posts = sc.textFile(input_fn_post)
    df_post = ((posts.map(lambda line: line.strip())
            .filter(lambda line: line.startswith('<row'))
            .filter(lambda line: '/>' in line)
            .map(Post.parse)
            .map(lambda x: (x.owneruserid,x.posttypeid,x.creationdate,x.score,
                            x.viewcount,x.answercount,x.favoritecount))
            .toDF(['ownerid','posttypeid','postcreationdate','score',
                   'views','answers','favorite'])))
    
    joined_7 = (df_post.join(df_user, df_post.ownerid == df_user.userid,'inner')
                   .withColumn('delta(days)',
                    (F.unix_timestamp('postcreationdate')-
                     F.unix_timestamp('usercreationdate'))/3600/24)
                   .withColumn('veterans', 
                     F.when(F.col('delta(days)').between(100,150), 1)
                      .otherwise(0)))
    
    veterans = (joined_7.filter(F.col('veterans') == 1)[['userid']]
                    .distinct())
    
    w = Window.partitionBy('ownerid').orderBy('postdate')

    vet = (joined_7.selectExpr('ownerid','posttypeid','postcreationdate as postdate',
                           'score','views','answers','favorite')
               .join(veterans, joined_7.ownerid == veterans.userid,'leftsemi')
               .filter(F.col('posttypeid') == 1)
               .withColumn('rn',F.row_number().over(w))
               .filter(F.col('rn') == 1)
               .agg({'score':'mean',
                     'views':'mean',
                     'answers':'mean',
                     'favorite':'mean'})
               .select(F.col('avg(score)').alias('vet_score'),
                       F.col('avg(views)').alias('vet_views'),
                       F.col('avg(answers)').alias('vet_answers'),
                       F.col('avg(favorite)').alias('vet_favorites')))

    stats_vet = vet.rdd.saveAsTextFile(output_fn_vet)
    
    brief = (joined_7.selectExpr('ownerid','posttypeid','postcreationdate as postdate',
                           'score','views','answers','favorite')
               .join(veterans, joined_7.ownerid == veterans.userid,'leftanti')
               .filter(F.col('posttypeid') == 1)
               .withColumn('rn',F.row_number().over(w))
               .filter(F.col('rn') == 1)
               .agg({'score':'mean',
                     'views':'mean',
                     'answers':'mean',
                     'favorite':'mean'})
               .select(F.col('avg(score)').alias('brief_score'),
                       F.col('avg(views)').alias('brief_views'),
                       F.col('avg(answers)').alias('brief_answers'),
                       F.col('avg(favorite)').alias('brief_favorites')))

    stats_brief = brief.rdd.saveAsTextFile(output_fn_brief)
    
    
if __name__ == '__main__':
    main(*sys.argv[1:])
