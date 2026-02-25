# KAFKA Docker compose
## Start Kafka locally with Docker Compose

![Create `docker/docker-compose.yml` with this](https://quix.io/docs/quix-streams/tutorials/docker-compose.yml)

Then run:
```bash
docker compose -f docker/docker-compose.yml up -d
```

Expected:
```bash
[+] Running 4/4
 ✔ Network docker_default     
 ✔ Container broker           
 ✔ Container schema-registry  
 ✔ Container control-center   Started   
```

Check logs:
```bash
docker ps
docker logs -f kafka
```

Check broker:
```bash
docker exec -it broker bash
# Expected: [appuser@broker ~]$ 
```

Check logs inside broker:
```bash
kafka-topics --list --bootstrap-server localhost:9092

# Expected: Several Internal Kafka Topics
```

To exit press `Ctrl + D`.

#### Open Confluent cluster localhost
```bash
http://localhost:9021/clusters
```

---
## CLosing Docker (inside a Docker folder)
```bash
docker compose -f docker/docker-compose.yml down -v
```