# kafka_streamcraft
A learning repository focused on building and understanding real-time data pipelines using Apache Kafka.
## 🎯 Goal of this repository

This repo is a **hands-on Kafka learning workspace**. The goal is to help start from zero and gradually practice:

- [Running Kafka with docker compose](https://quix.io/docs/quix-streams/tutorials/index.html#running-kafka-locally)
- [Producing and consuming messages](https://github.com/Akina-Aoki/data_platform_course/tree/main/08_producer_consumer)
- Understanding topics, partitions, offsets, and consumer groups
- Building simple streaming extendable workflows

---

## Prerequisites (install these first)

If you only have the GitHub repo right now, start by setting up your machine.

### Required tools

1. **Git** (to clone and manage your repository)
2. **Docker Desktop** (recommended, easiest way to run Kafka)
3. Python version 3.12.0. [Download if not yet available](https://www.python.org/downloads/release/python-3120/)

### References
- [Kafka Setup by Kokchun](https://www.youtube.com/watch?v=pqRebLFbmwI)
- [Github Kafka Setup](https://github.com/Akina-Aoki/data_platform_course/tree/main/07_kafka_setup)


---

## Clone repo from GitHub

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

## Create and activate Python 3.12 virtual environment
**For first time creating the venv
```bash
py -3.12 -m venv .venv
```

Activate:
```bash
source .venv/Scripts/activate
```

Sanity Check if venv is active:
```bash
which python
python --version
python -c "import sys; print(sys.prefix)
```

Expected just for this environement:
```bash
kafka_streamcraft\.venv
Python 3.12.10
```

CTRL + SHIFT + P → Select Interpreter. Choose
```bash
.venv (3.12.x)
```

### Install requirements
```bash
uv pip install quixstreams
```

Generate requirements after successfull install:
```bash
pip freeze > requirements.txt
``` 

---
 
## Documentatio Index
## 📚 Documentation

- [Producer & Consumer Explained](documentation/explain_producer_consumer.md)
- [Kafka Docker Setup](documentation/kafka_docker.md)
- [Producer–Consumer Workflow](documentation/workflow_producer_consumer.md)