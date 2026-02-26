"""Kafka producer that publishes realistic sample order events."""

import json
import random
import time
import uuid
from datetime import datetime, timedelta, timezone

from confluent_kafka import Producer

# Kafka broker connection settings.
producer_config = {
    "bootstrap.servers": "localhost:9092"
}

# Create a Kafka producer client using the config above.
producer = Producer(producer_config)

# A richer product catalog for practice scenarios.
PRODUCT_CATALOG = [
    {"sku": "ELEC-001", "name": "wireless earbuds", "category": "electronics", "unit_price": 89.99},
    {"sku": "ELEC-002", "name": "gaming mouse", "category": "electronics", "unit_price": 59.00},
    {"sku": "HOME-101", "name": "air fryer", "category": "home", "unit_price": 129.50},
    {"sku": "HOME-102", "name": "robot vacuum", "category": "home", "unit_price": 349.99},
    {"sku": "SPORT-201", "name": "yoga mat", "category": "sports", "unit_price": 32.00},
    {"sku": "SPORT-202", "name": "hiking bottle", "category": "sports", "unit_price": 24.75},
    {"sku": "GROC-301", "name": "protein bars pack", "category": "grocery", "unit_price": 18.99},
    {"sku": "GROC-302", "name": "cold brew concentrate", "category": "grocery", "unit_price": 15.50},
]

USERS = [
    {"user_id": "u-1001", "name": "Lara", "loyalty_tier": "gold", "region": "us-east"},
    {"user_id": "u-1002", "name": "Nora", "loyalty_tier": "silver", "region": "us-west"},
    {"user_id": "u-1003", "name": "Ethan", "loyalty_tier": "bronze", "region": "eu-central"},
    {"user_id": "u-1004", "name": "Priya", "loyalty_tier": "gold", "region": "ap-south"},
    {"user_id": "u-1005", "name": "Mateo", "loyalty_tier": "silver", "region": "us-east"},
]

PAYMENT_METHODS = ["card", "wallet", "bank_transfer", "cash_on_delivery"]
ORDER_STATUS = ["created", "paid", "packed", "shipped"]


def delivery_report(err, msg):
    """Print delivery status for each produced message."""
    if err:
        print(f"❌ Delivery failed: {err}")
    else:
        print(
            "✅ Delivered "
            f"order_id={msg.key().decode('utf-8')} "
            f"to {msg.topic()} | partition={msg.partition()} | offset={msg.offset()}"
        )


def generate_line_items():
    """Build a random list of line items with quantity and unit price."""
    items = random.sample(PRODUCT_CATALOG, k=random.randint(1, 4))
    line_items = []

    for product in items:
        quantity = random.randint(1, 5)
        line_items.append(
            {
                "sku": product["sku"],
                "name": product["name"],
                "category": product["category"],
                "quantity": quantity,
                "unit_price": product["unit_price"],
                "line_total": round(quantity * product["unit_price"], 2),
            }
        )

    return line_items


def generate_order_payload():
    """Generate a realistic order event for streaming practice."""
    user = random.choice(USERS)
    line_items = generate_line_items()

    subtotal = round(sum(item["line_total"] for item in line_items), 2)
    shipping_cost = round(random.choice([0.0, 4.99, 7.99, 12.99]), 2)
    discount = round(subtotal * random.choice([0.0, 0.05, 0.1]), 2)
    tax = round((subtotal - discount) * 0.08, 2)
    total_amount = round(subtotal - discount + tax + shipping_cost, 2)

    created_at = datetime.now(timezone.utc) - timedelta(minutes=random.randint(0, 30))

    return {
        "event_id": str(uuid.uuid4()),
        "event_type": "order.created",
        "event_version": "1.0",
        "event_time": created_at.isoformat(),
        "order": {
            "order_id": str(uuid.uuid4()),
            "status": random.choice(ORDER_STATUS),
            "currency": "USD",
            "payment_method": random.choice(PAYMENT_METHODS),
            "priority_shipping": random.choice([True, False]),
            "line_items": line_items,
            "charges": {
                "subtotal": subtotal,
                "discount": discount,
                "tax": tax,
                "shipping": shipping_cost,
                "total": total_amount,
            },
            "shipping_address": {
                "region": user["region"],
                "country": "US" if user["region"].startswith("us") else "IN",
            },
            "customer": {
                "user_id": user["user_id"],
                "name": user["name"],
                "loyalty_tier": user["loyalty_tier"],
            },
        },
        "metadata": {
            "source": "web",
            "campaign": random.choice(["summer_sale", "retargeting", "organic", "influencer"]),
            "trace_id": str(uuid.uuid4()),
        },
    }


def produce_sample_orders(total_orders=40, delay_seconds=0.1):
    """Publish a larger set of sample orders for stream processing practice."""
    for index in range(1, total_orders + 1):
        payload = generate_order_payload()
        order_id = payload["order"]["order_id"]

        producer.produce(
            topic="orders",
            key=order_id.encode("utf-8"),
            value=json.dumps(payload).encode("utf-8"),
            callback=delivery_report,
        )

        producer.poll(0)
        print(
            f"🛰️ Produced {index}/{total_orders} | "
            f"order_id={order_id} | total=${payload['order']['charges']['total']}"
        )

        if delay_seconds:
            time.sleep(delay_seconds)


if __name__ == "__main__":
    produce_sample_orders()
    producer.flush()
