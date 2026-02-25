"""Simple Kafka producer example for sending one order message."""

import json
import uuid

from confluent_kafka import Producer

# Kafka broker connection settings.
producer_config = {
    "bootstrap.servers": "localhost:9092"
}

# Create a Kafka producer client using the config above.
producer = Producer(producer_config)

def delivery_report(err, msg):
    """Print delivery status for each produced message."""
    # If Kafka returns an error, log the failure.
    if err:
        print(f"❌ Delivery failed: {err}")
    else:
        # Print the decoded message payload on success.
        print(f"✅ Delivered {msg.value().decode('utf-8')}")
        # Print destination metadata (topic, partition, offset).
        print(f"✅ Delivered to {msg.topic()} : partition {msg.partition()} : at offset {msg.offset()}")

# Sample order payload to publish.
order = {
    "order_id": str(uuid.uuid4()),
    "user": "lara",
    "item": "frozen yogurt",
    "quantity": 10
}

# Convert dict -> JSON string -> bytes for Kafka.
value = json.dumps(order).encode("utf-8")

# Send the message to the "orders" topic and register callback.
producer.produce(
    topic="orders",
    value=value,
    callback=delivery_report
)

# Block until all buffered messages are delivered.
producer.flush()