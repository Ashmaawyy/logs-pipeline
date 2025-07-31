# 🧠 Log Analysis Pipeline with Kafka, LLM, and PostgreSQL

A data engineering project that ingests log data using Apache Kafka, classifies it using a lightweight LLM, and stores only meaningful classified logs into PostgreSQL for further analysis. Ideal for handling large-scale logs in a resource-efficient way.

---

## 🚀 Project Overview

This pipeline allows you to:

- Ingest large log files in fast, batch-style Kafka producers.
- Use Kafka as a buffer to decouple ingestion and processing.
- Classify logs using an LLM to filter and extract only important entries.
- Store only relevant logs in PostgreSQL, reducing storage and processing overhead.
- Retain full raw logs in Kafka for future reprocessing or audits.

---

## 🧩 System Architecture

```

Logs Directory
        |
        v
Kafka Producer (Fast Batch Push)
        |
        v
Kafka Topic (raw\_logs)
        |
        v
Kafka Consumer + LLM Classifier (Lightweight)
        |
Filtered & Labeled Logs
        |
        v
PostgreSQL (Structured, Queryable Data)

```

---

## 🧠 Why Use LLM?

Instead of storing all raw logs in a database (which can be massive and noisy), an LLM can:

- Extract relevant information (errors, warnings, login attempts, attacks, etc.).
- Tag and classify log entries (e.g., Security Alert, App Error, Info).
- Let you focus your analysis only on useful log entries.

LLM suggestions can be implemented using:
- **LLM APIs** (e.g., OpenAI, Mistral) with short input context windows.
- **Lightweight models** like `distilbert`, `bge-small`, or rule-based NLP if needed offline.

---

## 🔧 Project Components

### Kafka Producer (batch_push_producer.py)
- Reads logs from a large file in chunks.
- Pushes batches to Kafka topic `raw_logs`.
- Fast and resource-light.

### Kafka Consumer (consumer_classifier.py)
- Subscribes to `raw_logs`.
- For each log entry, passes it to a lightweight LLM.
- If log is classified as “important,” stores in PostgreSQL.

### PostgreSQL
- Receives and stores classified logs.
- Schema includes: `timestamp`, `log_level`, `message`, `classification`, `source`.

---

## 📁 File Structure

```

log\_pipeline/
│
├── batch\_push\_producer.py         # Kafka producer script
├── consumer\_classifier.py         # Kafka consumer with LLM classifier
├── model\_utils.py                 # LLM classification logic
├── db\_utils.py                    # PostgreSQL connection and insert logic
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation

````

---

## 🛠️ Setup Instructions

### 1. Install Kafka
- Install and run Kafka on your machine or Docker (see Confluent or Bitnami images).

### 2. Set Up PostgreSQL
- Create a database and table with schema:
```sql
CREATE TABLE filtered_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ,
    log_level TEXT,
    message TEXT,
    classification TEXT,
    source TEXT
);
````

### 3. Create Kafka Topic

```bash
kafka-topics.sh --create --topic raw_logs --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### 4. Install Python Requirements

```bash
pip install -r requirements.txt
```

### 5. Run the Pipeline

* Start Kafka and Zookeeper
* Run the producer:

```bash
python batch_push_producer.py
```

* Run the consumer:

```bash
python consumer_classifier.py
```

---

## 📈 Example Use Case

For an Nginx log file like:

```
127.0.0.1 - - [30/Jul/2025:06:25:10 +0000] "GET /admin HTTP/1.1" 403 462
```

The pipeline could:

* Classify as `Security Alert`
* Store only this row in PostgreSQL:

```json
{
  "timestamp": "2025-07-30T06:25:10Z",
  "log_level": "WARNING",
  "message": "GET /admin returned 403",
  "classification": "Security Alert",
  "source": "nginx"
}
```

---

## 📌 Notes

* You can retain full logs in Kafka for compliance or reprocessing.
* LLMs should be limited to small batch inputs and can use offline models.
* Consider using LLM agents (e.g., LangChain) if future automation is needed.

---

## 📚 Future Enhancements

* Build a Streamlit dashboard to visualize filtered logs.
* Implement retraining of classifiers with feedback loop.
* Support multiple log formats (e.g., JSON, Apache, custom app logs).
* Add real-time alerts with keywords like “breach”, “denied”, “SQL”.

---

## 🧑‍💻 Author

Built by a Data Engineer eager to sharpen real-world data pipeline skills using modern tools.
Feel free to contribute or suggest enhancements!

---

## 📜 License

MIT License – use freely with attribution.