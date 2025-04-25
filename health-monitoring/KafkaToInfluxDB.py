from kafka import KafkaConsumer
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import json

# Replace with your actual credentials
bucket = "health-data"
org = "your-org-name"
token = "your-generated-token"
url = "http://localhost:8086"

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

consumer = KafkaConsumer(
    'health-data',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Kafka → InfluxDB is running...")
for message in consumer:
    data = message.value
    print("Received:", data)

    point = Point("health_metrics") \
        .field("heartbeat", data["heartbeat"]) \
        .field("steps", data["steps"]) \
        .field("calories", data["calories"])

    write_api.write(bucket=bucket, org=org, record=point)   

