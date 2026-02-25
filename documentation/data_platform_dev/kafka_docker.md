# Kafka Docker Compose (data_platform_dev)

This is the updated command workflow after moving the compose file to:

- `docker/data_platform_dev/docker-compose.yml`

And after removing fixed `container_name` values.

---

## 1) Pre-flight checks

```bash
# from repository root
pwd

# validate compose file
docker compose -f docker/data_platform_dev/docker-compose.yml config

# optional: check host ports used by this stack
ss -ltn '( sport = :9092 or sport = :9101 or sport = :8081 or sport = :9021 )'
```

If these ports are already occupied, stop the conflicting stack first.

---

## 2) Start Kafka stack

```bash
docker compose -p data_platform_dev -f docker/data_platform_dev/docker-compose.yml up -d
```

Expected services in this project:
- `broker`
- `schema-registry`
- `control-center`

---

## 3) Confirm startup status

```bash
docker compose -f docker/docker-compose.yml up -d
```

If you see `Created` on dependent services, wait a few seconds and run `up -d` again.

```bash
docker compose -p data_platform_dev -f docker/data_platform_dev/docker-compose.yml up -d
```

---

## 4) Read logs

```bash
docker ps
docker logs -f kafka
```

Check broker:
```bash
docker compose -p data_platform_dev -f docker/data_platform_dev/docker-compose.yml exec broker bash
```

Inside broker container:

```bash
kafka-topics --list --bootstrap-server localhost:9092
```

Exit shell with `Ctrl + D`.

---

## 6) Open Control Center

```bash
http://localhost:9021/clusters
```

---

## 7) Stop and cleanup stack

```bash
docker compose -p data_platform_dev -f docker/data_platform_dev/docker-compose.yml down -v
```

---

## Troubleshooting

### A) `container name "/broker" is already in use`

That came from old fixed-name containers. If you still have leftovers:

```bash
docker ps -a --filter name='^/broker$'
docker ps -a --filter name='^/schema-registry$'
docker ps -a --filter name='^/control-center$'

docker rm -f broker schema-registry control-center
```

### B) One service is `Up`, others are only `Created`

This usually means dependencies are still initializing. Check logs and retry:

```bash
docker compose -f docker/docker-compose.yml down -v
```

### C) Strange command like `[200~docker ...`

That is a terminal paste artifact (bracketed paste mode), not a Docker error. Re-type command once cleanly.
