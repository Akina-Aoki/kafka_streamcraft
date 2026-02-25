# Student guide: understanding `producer.py` and `consumer.py`

This is a beginner-friendly explanation of your Kafka demo using jokes data.

---

## Big picture (in simple terms)

Think of Kafka like a **message mailbox system**:

- **Producer** = the sender (puts messages into mailbox)
- **Topic** = the mailbox name (here: `jokes`)
- **Consumer** = the reader (takes messages from mailbox and processes them)

In this repository:

1. `producer.py` reads jokes from `data/jokes.json`
2. It sends each joke as a Kafka event into topic `jokes`
3. `consumer.py` reads those events from topic `jokes`
4. It transforms each joke into words and calculates each word length

---

## 1) What `producer.py` does

### Core code

```python
from quixstreams import Application
from pathlib import Path
import json

app = Application(broker_address="localhost:9092", consumer_group="text-splitter-v1")
jokes_topic = app.topic(name="jokes", value_serializer="json")

jokes_path = Path(__file__).parents[1] / "data" / "jokes.json"

with open(jokes_path, "r", encoding="utf-8") as file:
    jokes = json.load(file)


def main():
    print(app)
    with app.get_producer() as producer:
        for joke in jokes:
            joke["joke_id"] = str(joke["joke_id"])
            kafka_msg = jokes_topic.serialize(key=joke["joke_id"], value=joke)

            print(
                f"produce event with key = {kafka_msg.key}, value = {kafka_msg.value}"
            )

            producer.produce(
                topic=jokes_topic.name, key=kafka_msg.key, value=kafka_msg.value
            )


if __name__ == "__main__":
    main()
```

### Step-by-step explanation

- `Application(...)` connects your script to Kafka broker at `localhost:9092`.
- `app.topic(... value_serializer="json")` means Python dicts are converted to JSON bytes before sending.
- `jokes.json` is loaded into memory as a Python list of dictionaries.
- For each joke:
  - `joke_id` is converted to string and used as Kafka message key.
  - `serialize(...)` prepares key/value in Kafka-safe format.
  - `producer.produce(...)` sends the message to topic `jokes`.

### What the producer output means

When you see something like:

```text
produce event with key = b'1', value = b'{"joke_id":"1","joke_text":"Why did ..."}'
```

it means:

- `key = b'1'`: Kafka key for partitioning/order (bytes, therefore `b''`)
- `value = b'...'`: JSON payload as bytes
- One event has been produced to topic `jokes`

---

## 2) What `consumer.py` does

### Core code

```python
from quixstreams import Application

app = Application(
    broker_address="localhost:9092",
    consumer_group="text-splitter-v1",
    auto_offset_reset="earliest",
)

jokes_topic = app.topic(name="jokes", value_deserializer="json")
sdf = app.dataframe(topic=jokes_topic)

sdf = sdf.update(lambda message: print(f"Input: {message}"))

sdf = sdf.apply(
    lambda message: [{"word": word} for word in message["joke_text"].split()],
    expand=True,
)

sdf["length"] = sdf["word"].apply(lambda word: len(word))
sdf = sdf.update(lambda row: print(f"Output: {row}"))


if __name__ == "__main__":
    app.run()
```

### Step-by-step explanation

- `auto_offset_reset="earliest"` means: if this consumer group has no committed offsets yet, start from beginning of topic.
- `value_deserializer="json"` means incoming JSON bytes are converted back into Python dicts.
- `app.dataframe(...)` creates a streaming dataframe (`sdf`) from Kafka events.
- First `update(...)` prints each original message (`Input: ...`) as a side effect.
- `apply(... expand=True)` transforms one message into many rows:
  - it splits `joke_text` into words
  - each word becomes `{"word": <that_word>}`
- `sdf["length"] = ...` adds a computed column for word length.
- Final `update(...)` prints transformed rows (`Output: ...`).

### What consumer output means

If input is:

```text
Input: {'joke_id': '1', 'joke_text': 'Why did the data engineer break up ...'}
```

you then get many outputs, for example:

```text
Output: {'word': 'Why', 'length': 3}
Output: {'word': 'did', 'length': 3}
Output: {'word': 'engineer', 'length': 8}
```

This means your consumer is doing a **stream transformation**:

- one Kafka event in
- multiple derived records out
- each derived record is enriched with a calculated field

---

## 3) Why this matters for a data engineer

This small project demonstrates real data engineering patterns:

1. **Ingestion**
   - `producer.py` ingests source data (`jokes.json`) into Kafka topic.
2. **Streaming transformation**
   - `consumer.py` reads events continuously and transforms them.
3. **Schema-ish discipline**
   - You consistently use fields (`joke_id`, `joke_text`, `word`, `length`).
4. **Replayability**
   - With `earliest`, you can replay the full topic for testing or debugging.
5. **Scalability mindset**
   - Today it is jokes; tomorrow it can be clickstream, logs, payments, IoT telemetry.

In industry, this exact pattern becomes:

- Producer from apps / CDC / APIs
- Kafka as durable event backbone
- Consumers that clean, enrich, join, aggregate, and write to warehouses/lakes.

---

## 4) Key Kafka concepts mapped to your code

- **Broker**: Kafka server at `localhost:9092`
- **Topic**: `jokes`
- **Message key**: `joke_id` (string bytes)
- **Message value**: joke JSON
- **Consumer group**: `text-splitter-v1`
- **Offset**: message position in topic log
- **`earliest`**: start at beginning when no previous offset exists

---
