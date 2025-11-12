import time
from solace.messaging.messaging_service import MessagingService
from solace.messaging.resources.topic import Topic

# --- Solace Connection Configuration ---
BROKER_HOST = "tcp://solace:55555"
VPN_NAME = "default"
USERNAME = "admin"
PASSWORD = "admin"

# --- Initialize Messaging Service ---
print("🔌 Connecting to Solace PubSub+ broker...")

service = MessagingService.builder().from_properties({
    "solace.messaging.transport.host": BROKER_HOST,
    "solace.messaging.service.vpn-name": VPN_NAME,
    "solace.messaging.authentication.scheme.basic.username": USERNAME,
    "solace.messaging.authentication.scheme.basic.password": PASSWORD
}).build()

service.connect()
print("✅ Connected to Solace PubSub+ broker")

# --- Create Publisher ---
publisher = service.create_direct_message_publisher_builder().build()
publisher.start()
print("🚀 Publisher started. Sending messages...")

try:
    count = 0
    while True:
        topic = Topic.of("demo/topic")
        message = f"Hello World #{count}"
        publisher.publish(message=message, destination=topic)
        print(f"📨 Published: {message}")
        count += 1
        time.sleep(2)
except KeyboardInterrupt:
    print("\n🛑 Publisher stopped by user.")
finally:
    publisher.terminate()
    service.disconnect()
    print("🔒 Connection closed.")
