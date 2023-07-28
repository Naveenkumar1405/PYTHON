from flask import Flask, jsonify, request
import paho.mqtt.client as mqtt

app = Flask(__name__)

# MQTT configuration
MQTT_BROKER = "your_mqtt_broker_address"  # Replace with the IP address or hostname of your MQTT broker
MQTT_PORT = 1883
MQTT_TOPIC = "example_topic"  # Replace with the desired topic name

# MQTT client setup
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
mqtt_client.loop_start()  # Start a background thread to handle MQTT communication

# MQTT on_connect callback
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
    else:
        print("Connection failed. Return code =", rc)

# MQTT on_message callback
def on_message(client, userdata, message):
    print(f"Received message '{message.payload.decode()}' on topic '{message.topic}'")

# Register the callback functions with the MQTT client
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Set up an endpoint in your Flask API to publish a message to the MQTT broker
@app.route("/publish", methods=["POST"])
def publish_message():
    data = request.json
    if not data or "message" not in data:
        return jsonify({"error": "Invalid request data"}), 400

    message = data["message"]
    mqtt_client.publish(MQTT_TOPIC, message)
    return jsonify({"message": "Message published successfully"}), 200

# Function to subscribe to the MQTT topic within your Flask application
def subscribe_to_topic():
    mqtt_client.subscribe(MQTT_TOPIC)

# Call the subscribe_to_topic() function when the Flask app starts
subscribe_to_topic()

if __name__ == "__main__":
    app.run(debug=True)
