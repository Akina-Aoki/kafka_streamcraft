# kafka_streamcraft
A learning repository focused on building and understanding real-time data pipelines using Apache Kafka.
## 🎯 Goal of this repository

This repo is a **hands-on Kafka learning workspace**. The goal is to help start from zero and gradually practice:

- Running Kafka locally
- Producing and consuming messages
- Understanding topics, partitions, offsets, and consumer groups
- Building simple streaming extendable workflows

---

## Prerequisites (install these first)

If you only have the GitHub repo right now, start by setting up your machine.

### Required tools

1. **Git** (to clone and manage your repository)
2. **Docker Desktop** (recommended, easiest way to run Kafka)
3. **A code editor** (VS Code recommended)
4 **Terminal** (PowerShell, Command Prompt, iTerm, Bash, etc.)


---

## Clone your repo from GitHub

Replace `<your-github-username>` with your real username:

```bash
git clone https://github.com/<your-github-username>/kafka_streamcraft.git
cd kafka_streamcraft
```

Optional but useful:

```bash
git remote -v
```

You should see `origin` pointing to your GitHub repo.

---

## Create a local project structure

From inside `kafka_streamcraft`, create folders for cleaner learning:

```bash
mkdir -p docker notes labs scripts
```

Suggested purpose:

- `docker/` → Kafka + tools setup files
- `labs/` → your exercises
- `notes/` → what you learn each day
- `scripts/` → helper commands (topic creation, test data, etc.)

---


## Python dependencies for coding exercises

Since you'll use Python, set up a virtual environment and install Kafka client packages.

### Create and activate virtual environment

Install Python 3.10+ and then run:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

Sanity Check if venv is active:
```bash
which python
python -c "import sys; print(sys.prefix)
```

Expected:
```bash
kafka_streamcraft\.venv
```

## Requirements
In `requirements.txt`
```bash
confluent-kafka==2.4.0
kafka-python==2.0.2
pydantic==2.7.4
python-dotenv==1.0.1
```

Install dependencies:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pip list
```

Expected:
````bash
```

### Optional (helpful for experiments)

- Install extra package for easier local testing:

```bash
pip install kafka-python
```

`confluent-kafka` is the high-performance client you'll likely keep using. `kafka-python` can be easier when starting with simple scripts.

### Freeze dependencies for reproducibility

```bash
pip freeze > requirements.txt
```

Later, you can recreate your environment with:

```bash
pip install -r requirements.txt
```

--- 


# KAFKA
## Start Kafka locally with Docker Compose

Create `docker/docker-compose.yml` with this content:

```yaml
services:
  kafka:
    image: bitnami/kafka:3.7
    container_name: kafka
    ports:
      - "9092:9092"
    environment:
      - KAFKA_CFG_NODE_ID=0
      - KAFKA_CFG_PROCESS_ROLES=controller,broker
      - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093
      - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
      - KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER
      - KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@kafka:9093
      - KAFKA_CFG_AUTO_CREATE_TOPICS_ENABLE=true
      - KAFKA_CFG_OFFSETS_TOPIC_REPLICATION_FACTOR=1
      - KAFKA_CFG_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=1
      - KAFKA_CFG_TRANSACTION_STATE_LOG_MIN_ISR=1
      - ALLOW_PLAINTEXT_LISTENER=yes
```

Then run:

```bash
docker compose -f docker/docker-compose.yml up -d
```

Check logs:

```bash
docker logs -f kafka
```

When you see messages indicating Kafka is started, press `Ctrl + C`.

---

## Quick Kafka smoke test

### Create a topic

```bash
docker exec -it kafka kafka-topics.sh --create --topic first-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### List topics

```bash
docker exec -it kafka kafka-topics.sh --list --bootstrap-server localhost:9092
```

### Start a producer

```bash
docker exec -it kafka kafka-console-producer.sh --topic first-topic --bootstrap-server localhost:9092
```

Type a few messages and press Enter.

### Start a consumer (new terminal)

```bash
docker exec -it kafka kafka-console-consumer.sh --topic first-topic --from-beginning --bootstrap-server localhost:9092
```

If messages appear, your Kafka setup works ✅


---

# Suggested first-week learning roadmap

### 1
- Kafka basics (broker, topic, partition, offset)
- Run local Kafka and create topics

### 2
- Produce and consume messages manually
- Test `--from-beginning` and consumer groups

### 3
- Write first producer + consumer program
- Send JSON messages

### 4
- Create multiple partitions and observe ordering
- Try two consumers in one group

### 5
- Add retry/error handling
- Save your learnings in `notes/`
