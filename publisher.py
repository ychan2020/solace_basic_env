import time
import json
import random
import logging
from solace.messaging.messaging_service import MessagingService
from solace.messaging.resources.topic import Topic

# --- Configure Logging ---
logging.basicConfig(
    filename="publisher.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# --- Solace Connection Configuration ---
BROKER_HOST = "tcp://solace:55555"
VPN_NAME = "default"
USERNAME = "admin"
PASSWORD = "admin"

# --- Connect to Solace ---
logging.info("🔌 Connecting to Solace PubSub+ broker...")

service = MessagingService.builder().from_properties({
    "solace.messaging.transport.host": BROKER_HOST,
    "solace.messaging.service.vpn-name": VPN_NAME,
    "solace.messaging.authentication.scheme.basic.username": USERNAME,
    "solace.messaging.authentication.scheme.basic.password": PASSWORD
}).build()

service.connect()
logging.info("✅ Connected to Solace PubSub+ broker")

# --- Create Publisher ---
publisher = service.create_direct_message_publisher_builder().build()
publisher.start()
logging.info("🚀 Publisher started. Publishing simulated currency exchange rates...")

# --- Base rates for simulation ---
base_rates = {
    "EUR": 0.86,
    "GBP": 0.76,
    "JPY": 154.69,
    "KRW": 1467.02,
    "HKD": 7.77,
    "INR": 88.63
}

try:
    while True:
        # --- Simulate small random changes (+/-0.1%) ---
        simulated_rates = {k: v * (1 + random.uniform(-0.001, 0.001)) for k, v in base_rates.items()}

        # --- Create message ---
        timestamp = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
        message_data = {
            "base": "USD",
            "timestamp": timestamp,
            "rates": simulated_rates
        }

        message_json = json.dumps(message_data)
        topic = Topic.of("fx/rates/USD")

        # --- Publish to Solace ---
        publisher.publish(message=message_json, destination=topic)
        logging.info(f"📨 Published: {message_json}")

        # --- Wait 10 seconds before next publish ---
        time.sleep(1)

except KeyboardInterrupt:
    logging.info("🛑 Publisher stopped by user.")

except Exception as e:
    logging.error(f"❌ Unexpected error: {e}", exc_info=True)

finally:
    publisher.terminate()
    service.disconnect()
    logging.info("🔒 Connection closed.")
