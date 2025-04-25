3.	prediction.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StringType
import joblib

model = joblib.load('health_model.pkl')  # Ensure the path to the model is correct

def predict_health(heartbeat, steps, calories):
    # Prepare the features for prediction
    features = [[heartbeat, steps, calories]]
    # Get prediction from the model (0 - unhealthy, 1 - healthy)
    prediction = model.predict(features)
    return "healthy" if prediction[0] == 1 else "unhealthy"

spark = SparkSession.builder \
    .appName("HealthStatusPrediction") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "health-data") \
    .load()

df = df.selectExpr("CAST(value AS STRING)")

json_schema = StringType()
df = df.withColumn("json", from_json(col("value"), "heartbeat INT, steps INT, calories DOUBLE"))

df = df.select("json.heartbeat", "json.steps", "json.calories")


predict_udf = udf(predict_health, StringType())


df = df.withColumn("health_status", predict_udf(col("heartbeat"), col("steps"), col("calories")))


query = df.select("heartbeat", "steps", "calories", "health_status") \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()


query.awaitTermination()
