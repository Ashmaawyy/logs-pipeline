from kafka import KafkaConsumer
import psycopg2
import openai  # Or any LLM provider (e.g., transformers for local models)
import json
import logging

# -- Setting up logging --
logging.basicConfig(
    level=logging.INFO,
    format="🕒 %(asctime)s - 📍 %(name)s - [%(levelname)s]  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# -- Kafka Setup --
KAFKA_TOPIC = "logs-topic"
KAFKA_BOOTSTRAP = "localhost:9092"

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP,
    auto_offset_reset='latest',  # or 'earliest'
    enable_auto_commit=True,
    group_id='log-analyzer',
    value_deserializer=lambda x: x.decode('utf-8')
)

# -- PostgreSQL Setup --
pg_conn = psycopg2.connect(
    host="localhost",
    database="logdb",
    user="your_user",
    password="your_password"
)
pg_cursor = pg_conn.cursor()

# -- OpenAI Setup (Replace with your API key) --
openai.api_key = "sk-..."  # move to env variable in production

# -- Create PostgreSQL Table --
pg_cursor.execute("""
CREATE TABLE IF NOT EXISTS log_classifications (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    original_line TEXT,
    classification TEXT,
    summary TEXT
);
""")
pg_conn.commit()

# -- LLM Classifier Function --
def classify_log_line(log_line):
    prompt = f"""
You are a log analysis assistant. Given this log line:

{log_line}

1. Classify the log as one of: INFO, WARNING, ERROR, CRITICAL, OTHER
2. Briefly summarize what it means in plain English.

Respond in JSON like:
{{
  "classification": "ERROR",
  "summary": "Database connection failed."
}}
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or any other model
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    result = response.choices[0].message.content.strip()
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return {"classification": "OTHER", "summary": "Could not parse"}

# -- Consumer Logic --
for message in consumer:
    log_line = message.value
    result = classify_log_line(log_line)

    # Save classification (not full log) to PostgreSQL
    pg_cursor.execute(
        "INSERT INTO log_classifications (original_line, classification, summary) VALUES (%s, %s, %s)",
        (log_line, result["classification"], result["summary"])
    )
    pg_conn.commit()

    logging.info(f"✅ Stored: {result['classification']} - {result['summary']}")
