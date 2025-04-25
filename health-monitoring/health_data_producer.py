health_data_producer.py  
import json
import random
import time
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_health_data():
    return {
        "heartbeat": random.randint(60, 120),
        "steps": random.randint(100, 1000),
        "calories": round(random.uniform(100, 400), 2)
    }

while True:
    data = generate_health_data()
    print("Sending:", data)
    producer.send('health-data', value=data)
    time.sleep(2)
