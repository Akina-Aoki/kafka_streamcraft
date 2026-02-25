# Producer and consumer workflow

## Producer and consumer overview

<img src="https://github.com/kokchun/assets/blob/main/data_platform/producer_consumer_theory.png?raw=true" alt="kafka producer consumer" width="600">

After you run producer and consumer:

<img src="https://github.com/kokchun/assets/blob/main/data_platform/producer_consumer.png?raw=true" alt="kafka producer consumer" width="600">

---

## 0) Start Kafka stack first

```bash
docker compose -p data_platform_dev -f docker/data_platform_dev/docker-compose.yml up -d
docker compose -p data_platform_dev -f docker/data_platform_dev/docker-compose.yml ps
```

---

## 1) Consume data from topic in broker

Open broker container shell (new workflow):

```bash
docker compose -p data_platform_dev -f docker/data_platform_dev/docker-compose.yml exec broker bash
```

Then run consumer command:

```bash
kafka-console-consumer --bootstrap-server localhost:9092 --topic <topic_name> --from-beginning
```

Example:

```bash
kafka-console-consumer --bootstrap-server localhost:9092 --topic jokes --from-beginning --property print.key=true --property print.timestamp=true
```

---

## 2) Run Python producer/consumer app

From repository root:

```bash
source .venv/Scripts/activate  # Git Bash on Windows
python src/data_platform_dev/producer.py
python src/data_platform_dev/consumer.py
```

---

## 3) Useful checks

```bash
docker compose -p data_platform_dev -f docker/data_platform_dev/docker-compose.yml logs --tail=200 broker
docker compose -p data_platform_dev -f docker/data_platform_dev/docker-compose.yml logs --tail=200 schema-registry control-center
```

---

## Resources
- [kafka fundamentals - conduktor kafkacademy](https://learn.conduktor.io/kafka/kafka-fundamentals/)
- [kafka topics - conduktor kafkacademy](https://learn.conduktor.io/kafka/kafka-topics/)
- [kafka producers - conduktor kafkacademy](https://learn.conduktor.io/kafka/kafka-producers/)
- [kafka consumers - conduktor kafkacademy](https://learn.conduktor.io/kafka/kafka-consumers/)
