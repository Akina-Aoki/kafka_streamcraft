"""Simple Kafka consumer that tracks and prints incoming order messages."""

import json

from confluent_kafka import Consumer

# Kafka consumer connection and behavior settings.
consumer_config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "order-tracker",
    "auto.offset.reset": "earliest"
}

# Create a Kafka consumer client.
consumer = Consumer(consumer_config)

# Subscribe this consumer to the orders topic.
consumer.subscribe(["orders"])

print("🟢 Consumer is running and subscribed to orders topic")

try:
    # Keep listening for new messages until interrupted.
    while True:
        # Poll Kafka for one message (wait up to 1 second).
        msg = consumer.poll(1.0)
        # If no message was received, keep polling.
        if msg is None:
            continue
        # If broker returned an error, print it and continue.
        if msg.error():
            print("❌ Error:", msg.error())
            continue

        # Decode message bytes to text and parse JSON payload.
        value = msg.value().decode("utf-8")
        order = json.loads(value)
        # Print a quick summary of the received order.
        print(f"📦 Received order: {order['quantity']} x {order['item']} from {order['user']}")
except KeyboardInterrupt:
    # Handle Ctrl+C gracefully.
    print("\n🔴 Stopping consumer")

finally:
    # Close consumer to commit offsets and clean up resources.
    consumer.close()