from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, IntegerType

spark = SparkSession.builder.appName("HealthMonitor").getOrCreate()

schema = StructType([
    StructField("heart_rate", IntegerType(), True),
    StructField("steps", IntegerType(), True),
    StructField("calories", IntegerType(), True)
])

df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "health-data-stream") \
    .load()

df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

df.writeStream.outputMode("append").format("console").start().awaitTermination()
