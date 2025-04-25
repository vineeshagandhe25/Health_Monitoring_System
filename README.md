
Real-Time Health Monitoring System with Kafka, Spark, and Grafana

This project simulates real-time health data, processes it using Apache Spark and a Machine Learning model, stores the data in InfluxDB, and visualizes metrics using Grafana.
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Tech Stack
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
WSL2 (Ubuntu)
Apache Kafka
Apache Spark
Python (with kafka-python, Twilio SDK)
InfluxDB
Grafana
Twilio API (for alerts)
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Setup Guide
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Step 1: Install Prerequisites
- Enable WSL2 and install Ubuntu:  
wsl --install
sudo apt update && sudo apt upgrade

Step 2: Install Required Tools
- Install Java: sudo apt install openjdk-11-jdk -y
java -version
- Download and extract Kafka: 
wget https://downloads.apache.org/kafka/4.0.0/kafka_2.13-4.0.0.tgz
tar -xvzf kafka_2.13-4.0.0.tgz
mv kafka_2.13-4.0.0 kafka
cd kafka
- Format Kafka storage and start server: 
./bin/kafka-storage.sh random-uuid
./bin/kafka-storage.sh format -t <cluster-id> -c config/kraft/server.properties
./bin/kafka-server-start.sh config/kraft/server.properties

Step 3: Simulate Health Data Producer
- Install Kafka Python client: pip install kafka-python
- Create Kafka topic:
./bin/kafka-topics.sh --create --topic healthdata --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
- Run the producer script:
python3 producer.py

Step 4: Spark Streaming & ML Model
- Install Apache Spark:
wget https://downloads.apache.org/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz
tar -xvzf spark-3.5.0-bin-hadoop3.tgz
mv spark-3.5.0-bin-hadoop3 spark
- Add Spark to your environment:
  export SPARK_HOME=~/spark
  export PATH=$PATH:$SPARK_HOME/bin
  source ~/.bashrc


- Run Spark application:
  spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.0 spark_health_data_consumer.py

Step 5: InfluxDB Setup
- Install InfluxDB:
  wget https://dl.influxdata.com/influxdb/releases/influxdb2-2.0.8-amd64.deb
  sudo dpkg -i influxdb2-2.0.8-amd64.deb
  sudo systemctl start influxdb
  sudo systemctl enable influxdb
- Access at: [http://localhost:8086](http://localhost:8086)

Step 6: Grafana Setup
- Install Grafana:
  sudo apt-get install -y software-properties-common gnupg
  sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
  wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
  sudo apt-get update
  sudo apt-get install grafana
  sudo systemctl start grafana-server
  sudo systemctl enable grafana-server
- Access at: [http://localhost:3000](http://localhost:3000)  
  Default credentials: `admin / admin`

Step 7: Grafana + InfluxDB Integration

- In Grafana, add InfluxDB as a data source:
  - URL: `http://localhost:8086`
  - Query Language: `Flux`
  - Organization, Token, Bucket: (your InfluxDB credentials)

Step 8: Display Health Metrics
- Create a Grafana dashboard.
- Example Flux query to show heart rate:
  from(bucket: "health-data")
    |> range(start: -5m)
    |> filter(fn: (r) => r._measurement == "health_metrics")
    |> filter(fn: (r) => r._field == "heart_rate")

Step 9: SMS Alerts using Twilio
- Install Twilio SDK:
  pip install twilio
- Create and run Twilio alert script in Python:
  python3 alert_twilio.py

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------  
Project Structure
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
├── kafka/
├── spark/
│   └── spark_health_data_consumer.py
├── producer.py
├── prediction.py
├── grafana/
├── influxdb/
├── alert_twilio.py
└── README.md

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Outputs
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
- Real-time health data streaming through Kafka
- Spark Streaming with ML predictions
- Interactive dashboards in Grafana
- Alerts for abnormal health values via Twilio SMS
