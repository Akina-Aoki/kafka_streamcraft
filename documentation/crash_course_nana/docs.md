# Learning Kafka + Docker with hands-on project

## References
[Docker Image used for this project](https://hub.docker.com/layers/confluentinc/cp-kafka/7.8.3/images/sha256-f7351796d5598ffc1161d24a4ce8cf02be1696e456d859bd49cbb94bd2c038e8)


## Spinning up Kafka in Docker
Validate compose:
```
docker compose -f docker/crash_course_nana/docker-compose.yml config
```

Start only this specific project. One project at a time:
```
docker compose -p crash_course_nana -f docker/crash_course_nana/docker-compose.yml up -d
```

Expected:
```
[+] Running 3/3
 ✔ Network crash_course_nana_default
 ✔ Volume crash_course_nana_kafka_kraft 
 ✔ Container kafka 
```

Check status:
```
docker compose -p crash_course_nana -f docker/crash_course_nana/docker-compose.yml ps -a
```

Check logs:
```
docker compose -p crash_course_nana \
  -f docker/crash_course_nana/docker-compose.yml \
  logs --tail=200 kafka
```

Check the services:
```
docker compose -p crash_course_nana \
  -f docker/crash_course_nana/docker-compose.yml \
  logs kafka
```


Check if broker is running
```
docker compose -p crash_course_nana \
  -f docker/crash_course_nana/docker-compose.yml up -d
```
Expected:
```
[+] Running 1/1
 ✔ Container kafka  Running   
```

exec into broker shell:
```
docker compose -p crash_course_nana \
  -f docker/crash_course_nana/docker-compose.yml \
  exec kafka bash
```


IMPORTANT. Dont forget to close the docker container so the port won't collide. Stop this project:
```
docker compose -p crash_course_nana -f docker/crash_course_nana/docker-compose.yml down -v
```