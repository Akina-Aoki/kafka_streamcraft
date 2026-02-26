"""Kafka consumer that tracks order stream metrics and anomalies."""

import json
from collections import Counter, defaultdict

from confluent_kafka import Consumer

# Kafka consumer connection and behavior settings.
consumer_config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "order-tracker",
    "auto.offset.reset": "earliest",
}

# Create a Kafka consumer client.
consumer = Consumer(consumer_config)

# Subscribe this consumer to the orders topic.
consumer.subscribe(["orders"])

# Running analytics state to mimic real stream processing use cases.
state = {
    "processed_orders": 0,
    "gross_revenue": 0.0,
    "status_counts": Counter(),
    "region_revenue": defaultdict(float),
    "payment_method_counts": Counter(),
    "high_value_alerts": 0,
}

HIGH_VALUE_THRESHOLD = 500.00
print("🟢 Consumer is running and subscribed to orders topic")


def process_order_event(event):
    """Update stream analytics based on incoming order payload."""
    order = event["order"]
    charges = order["charges"]
    customer = order["customer"]
    region = order["shipping_address"]["region"]

    total = float(charges["total"])
    state["processed_orders"] += 1
    state["gross_revenue"] += total
    state["status_counts"][order["status"]] += 1
    state["region_revenue"][region] += total
    state["payment_method_counts"][order["payment_method"]] += 1

    print(
        "📦 Order "
        f"{order['order_id']} | customer={customer['name']} ({customer['loyalty_tier']}) "
        f"| items={len(order['line_items'])} | total=${total:.2f} | status={order['status']}"
    )

    if total >= HIGH_VALUE_THRESHOLD:
        state["high_value_alerts"] += 1
        print(
            "🚨 High-value order detected "
            f"(>${HIGH_VALUE_THRESHOLD:.0f}): order_id={order['order_id']} total=${total:.2f}"
        )

    if state["processed_orders"] % 10 == 0:
        top_region, top_revenue = max(
            state["region_revenue"].items(), key=lambda item: item[1]
        )
        top_payment, top_count = state["payment_method_counts"].most_common(1)[0]

        print("\n📊 Stream checkpoint")
        print(f"   Orders processed: {state['processed_orders']}")
        print(f"   Gross revenue: ${state['gross_revenue']:.2f}")
        print(f"   Top region by revenue: {top_region} (${top_revenue:.2f})")
        print(f"   Preferred payment method: {top_payment} ({top_count} orders)")
        print(f"   Status distribution: {dict(state['status_counts'])}")
        print(f"   High-value alerts: {state['high_value_alerts']}\n")


try:
    # Keep listening for new messages until interrupted.
    while True:
        # Poll Kafka for one message (wait up to 1 second).
        msg = consumer.poll(1.0)
        if msg is None:
            continue

        if msg.error():
            print("❌ Error:", msg.error())
            continue

        try:
            value = msg.value().decode("utf-8")
            event = json.loads(value)
            process_order_event(event)
        except (json.JSONDecodeError, KeyError, TypeError) as err:
            print(f"⚠️ Skipping malformed message: {err}")
except KeyboardInterrupt:
    # Handle Ctrl+C gracefully.
    print("\n🔴 Stopping consumer")

finally:
    # Close consumer to commit offsets and clean up resources.
    consumer.close()
