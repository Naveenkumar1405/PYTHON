import paho.mqtt.client as mqtt
import json

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Your MQTT topics and data
topics_and_data = {
    "onwords/3chfb008/status": {'id': '3chfb008', 'device1': True, 'device2': True, 'device3': True},
    "onwords/3chfb009/status": {'id': '3chfb009', 'device1': True, 'device2': True, 'device3': True},
    "onwords/3chfb006/status": {'id': '3chfb006', 'device1': True, 'device2': True, 'device3': True},
    "onwords/3chfb004/status": {'id': '3chfb004', 'device1': True, 'device2': True, 'device3': True},
    "onwords/3chfb001/status": {'id': '3chfb001', 'device1': True, 'device2': True, 'device3': True},
}

@app.route("/")
def index():
    devices = []
    for topic, data in topics_and_data.items():
        device = {
            "id": data["id"],
            "device1": data["device1"],
            "device2": data["device2"],
            "device3": data["device3"],
        }
        devices.append(device)

    return render_template("index.html", devices=devices)

@app.route("/api/devices")
def devices():
    return jsonify(topics_and_data)

def on_message(client, userdata, message):
    print("message received: " + message.topic + " " + message.payload.decode("utf-8"))

if __name__ == "__main__":
    broker_address = "mqtt.onwordsapi.com"
    broker_port = 1883
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(broker_address, broker_port)

    for topic, data in topics_and_data.items():
        message = json.dumps(data)
        client.publish(topic, message)
    
    # Run the Flask app
    app.run(debug=True)
