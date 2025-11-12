from solace.messaging.messaging_service import MessagingService
from solace.messaging.resources.topic_subscription import TopicSubscription

# --- Solace Connection Configuration ---
BROKER_HOST = "tcp://solace:55555"
VPN_NAME = "default"
USERNAME = "admin"
PASSWORD = "admin"

# --- Initialize Messaging Service ---
service = MessagingService.builder().from_properties({
    "solace.messaging.transport.host": BROKER_HOST,
    "solace.messaging.service.vpn-name": VPN_NAME,
    "solace.messaging.authentication.scheme.basic.username": USERNAME,
    "solace.messaging.authentication.scheme.basic.password": PASSWORD
}).build()

service.connect()
print("✅ Connected to Solace broker")

# --- Define subscription ---
subscription = TopicSubscription.of("demo/topic")

# --- Create Subscriber ---
receiver = (
    service.create_direct_message_receiver_builder()
    .with_subscriptions([subscription])  # must be a list
    .build()
)

receiver.start()
print("🎧 Subscriber started. Listening for messages...")

try:
    while True:
        msg = receiver.receive_message(timeout=1)  # wait up to 1 second for a message
        if msg:
            print(f"📩 Received message: {msg.get_payload_as_string()}")
except KeyboardInterrupt:
    print("\n🛑 Subscriber stopped by user.")
finally:
    receiver.terminate()
    service.disconnect()
    print("🔒 Connection closed.")
