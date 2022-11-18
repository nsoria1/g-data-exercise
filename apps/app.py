#pyspark --packages org.apache.spark:spark-avro_2.12:3.3.1 --jars postgresql-42.5.0.jar
from pyspark.sql import SparkSession

spark = SparkSession.builder.config("spark.jars", "postgresql-42.5.0.jar").master("local").appName("postgres").getOrCreate()
#spark = SparkSession.builder.master("local").appName("postgres").getOrCreate()

df = spark.read.format("jdbc").option("url", "jdbc:postgresql://localhost:5432/data") \
    .option("driver", "org.postgresql.Driver").option("dbtable", "jobs") \
    .option("user", "globant").option("password", "globant").load()

df.show()
#df.write.format('avro').mode('overwrite').save('/data/jobs')

# df.write.format("jdbc") \
#     .option("url", "jdbc:postgresql://localhost:5432/data") \
#     .option("driver", "org.postgresql.Driver").option("dbtable", "jobs2") \
#     .option("user", "globant").option("password", "globant").save()