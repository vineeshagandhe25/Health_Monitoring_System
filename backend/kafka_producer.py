from kafka import KafkaProducer
import json
from google_fit_api import fetch_health_data

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def send_data_to_kafka():
    health_data = fetch_health_data()
    producer.send('health-data-stream', health_data)
    print("Data Sent!")