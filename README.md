# kafka_streamcraft
A learning repository focused on building and understanding real-time data pipelines using Apache Kafka.
## 🎯 Goal of this repository

This repo is a **hands-on Kafka learning workspace**. The goal is to help start from zero and gradually practice:

- ![Running Kafka with docker compose](https://quix.io/docs/quix-streams/tutorials/index.html#running-kafka-locally)
- Producing and consuming messages
- Understanding topics, partitions, offsets, and consumer groups
- Building simple streaming extendable workflows

---

## Prerequisites (install these first)

If you only have the GitHub repo right now, start by setting up your machine.

### Required tools

1. **Git** (to clone and manage your repository)
2. **Docker Desktop** (recommended, easiest way to run Kafka)

### References
- ![Kafka Setup by Kokchun](https://www.youtube.com/watch?v=pqRebLFbmwI)
- ![Github Kafka Setup](https://github.com/Akina-Aoki/data_platform_course/tree/main/07_kafka_setup)


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


## Python dependencies for coding exercises

Since you'll use Python, set up a virtual environment and install Kafka client packages.

### Create and activate virtual environment
**For first time creating the venv
```bash
python -m venv .venv
```

Activate:
```bash
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

--- 

