from kafka import KafkaProducer
import time
import random

LOG_FILE = 'sample_logs/app.log'
TOPIC = 'logs-topic'

producer = KafkaProducer(bootstrap_servers='localhost:9092')

def stream_logs():
    with open(LOG_FILE, 'r') as f:
        logs = f.readlines()

    while True:
        log = random.choice(logs).strip()
        producer.send(TOPIC, log.encode('utf-8'))
        print(f"Sent: {log}")
        time.sleep(1)

if __name__ == "__main__":
    stream_logs()
