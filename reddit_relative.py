import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('reddit relative scores').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

comments_schema = types.StructType([
    types.StructField('archived', types.BooleanType()),
    types.StructField('author', types.StringType()),
    types.StructField('author_flair_css_class', types.StringType()),
    types.StructField('author_flair_text', types.StringType()),
    types.StructField('body', types.StringType()),
    types.StructField('controversiality', types.LongType()),
    types.StructField('created_utc', types.StringType()),
    types.StructField('distinguished', types.StringType()),
    types.StructField('downs', types.LongType()),
    types.StructField('edited', types.StringType()),
    types.StructField('gilded', types.LongType()),
    types.StructField('id', types.StringType()),
    types.StructField('link_id', types.StringType()),
    types.StructField('name', types.StringType()),
    types.StructField('parent_id', types.StringType()),
    types.StructField('retrieved_on', types.LongType()),
    types.StructField('score', types.LongType()),
    types.StructField('score_hidden', types.BooleanType()),
    types.StructField('subreddit', types.StringType()),
    types.StructField('subreddit_id', types.StringType()),
    types.StructField('ups', types.LongType()),
    #types.StructField('year', types.IntegerType()),
    #types.StructField('month', types.IntegerType()),
])


def main(in_directory, out_directory):
    comments = spark.read.json(in_directory, schema=comments_schema)
    comments = comments.cache()
    # TODO
    # 1
    sub_reddit_avg = comments.groupBy('subreddit').agg(functions.avg('score'))
    # 2
    filtered_subreddits = sub_reddit_avg.filter(sub_reddit_avg['avg(score)']>0).cache()
    
    # 3
    comments_avg = comments.join(filtered_subreddits.hint("broadcast"), on='subreddit')
    comments_rel_score = comments_avg.withColumn('rel_score',comments_avg['score']/comments_avg['avg(score)']).cache()
    # 4
    max_rel_scores = comments_rel_score.groupBy('subreddit').agg(functions.max('rel_score').alias('rel_score'))

    # 5
    best_author = comments_rel_score.join(max_rel_scores.hint("broadcast"), ['subreddit', 'rel_score'])
    best_author = best_author.select('subreddit', 'author', 'rel_score')
    
    best_author.write.json(out_directory, mode='overwrite')

if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)