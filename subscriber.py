import json
import threading
import time
from flask import Flask, render_template_string
from solace.messaging.messaging_service import MessagingService
from solace.messaging.receiver.message_receiver import MessageHandler
from solace.messaging.resources.topic_subscription import TopicSubscription

# --- Solace Connection Configuration ---
BROKER_HOST = "tcp://solace:55555"
VPN_NAME = "default"
USERNAME = "admin"
PASSWORD = "admin"
TOPIC_NAME = "fx/rates/USD"

# --- Flask App ---
app = Flask(__name__)

# --- Shared Data ---
latest_rates = {}
previous_rates = {}
lock = threading.Lock()  # protect shared data

# --- HTML Template ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Currency Rates Dashboard</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #fafafa; color: #333; }
        h1 { text-align: center; }
        table { margin: 0 auto; border-collapse: collapse; width: 60%; }
        th, td { padding: 12px 20px; text-align: center; border-bottom: 1px solid #ccc; font-size: 1.2em; }
        .up { color: green; font-weight: bold; }
        .down { color: red; font-weight: bold; }
        .same { color: gray; }
    </style>
</head>
<body>
    <h1>💱 USD Exchange Rates</h1>
    <table>
        <tr><th>Currency</th><th>Rate</th><th>Change</th></tr>
        {% for currency, rate_info in rates.items() %}
            <tr>
                <td>{{ currency }}</td>
                <td class="{{ rate_info.trend }}">{{ rate_info.value }}</td>
                <td class="{{ rate_info.trend }}">
                    {% if rate_info.trend == 'up' %}🔼{% elif rate_info.trend == 'down' %}🔻{% else %}–{% endif %}
                </td>
            </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route("/")
def index():
    display_data = {}
    with lock:
        for cur, rate in latest_rates.items():
            prev = previous_rates.get(cur)
            if prev is None:
                trend = "same"
            elif rate > prev:
                trend = "up"
            elif rate < prev:
                trend = "down"
            else:
                trend = "same"

            display_data[cur] = {"value": f"{rate:.4f}", "trend": trend}

    return render_template_string(HTML_TEMPLATE, rates=display_data)

# --- Solace Subscriber Thread ---
def start_subscriber():
    global latest_rates, previous_rates

    service = MessagingService.builder().from_properties({
        "solace.messaging.transport.host": BROKER_HOST,
        "solace.messaging.service.vpn-name": VPN_NAME,
        "solace.messaging.authentication.scheme.basic.username": USERNAME,
        "solace.messaging.authentication.scheme.basic.password": PASSWORD
    }).build()

    service.connect()
    print("✅ Connected to Solace broker as subscriber")

    receiver = (
        service.create_direct_message_receiver_builder()
        .with_subscriptions([TopicSubscription.of(TOPIC_NAME)])
        .build()
    )
    receiver.start()
    print(f"📡 Subscribed to topic: {TOPIC_NAME}")
    print(f"Broker host: {BROKER_HOST}, VPN: {VPN_NAME}, user: {USERNAME}")

    class Handler(MessageHandler):
        def on_message(self, message):
            global latest_rates, previous_rates
            try:
                payload = message.get_payload_as_string()
                data = json.loads(payload)
                rates = data.get("rates", {})

                with lock:
                    previous_rates = latest_rates.copy()
                    latest_rates = rates

                print(f"📩 Received update: {rates}")
            except Exception as e:
                print(f"❌ Error processing message: {e}")

    receiver.receive_async(Handler())

    while True:
        time.sleep(1)

# --- Main Entry ---
if __name__ == "__main__":
    thread = threading.Thread(target=start_subscriber, daemon=True)
    thread.start()

    app.run(host="0.0.0.0", port=5000, debug=False)
