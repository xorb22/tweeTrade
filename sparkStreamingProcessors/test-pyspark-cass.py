from pyspark import SparkConf, SparkContext
import pyspark_cassandra
from pyspark_cassandra import CassandraSparkContext

conf = SparkConf()\
	.setAppName("PySpark Cassandra Test") \
	.setMaster("local[2]") \
        .set("spark.cassandra.connection.host","52.25.173.31, 35.165.251.179, 52.27.187.234, 52.38.246.84")
#	.set("spark.cassandra.connection.host","52.25.173.31, 35.165.251.179, 52.27.187.234, 52.38.246.84")


sc = CassandraSparkContext(conf=conf)
print((sc.cassandraTable("tweetdb", "tweettable").select("tweet").map(lambda a: a).collect()))
#sc.pprint()

#rdd = sc.parallelize([{"tweet":"first second third tweet"}])

#rdd.saveToCassandra(
#	"tweetdb",
#	"tweettable")
