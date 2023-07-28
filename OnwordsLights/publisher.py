import paho.mqtt.client as mqtt
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

topics_and_data = {
    "onwords/3chfb008/status": {'id': '3chfb008', 'device1': True, 'device2': True, 'device3': True},
    "onwords/3chfb009/status": {'id': '3chfb009', 'device1': True, 'device2': True, 'device3': True},
    "onwords/3chfb006/status": {'id': '3chfb006', 'device1': True, 'device2': True, 'device3': True},
    "onwords/3chfb004/status": {'id': '3chfb004', 'device1': True, 'device2': True, 'device3': True},
    "onwords/3chfb001/status": {'id': '3chfb001', 'device1': True, 'device2': True, 'device3': True},
}

client = mqtt.Client()
client.connect("mqtt.onwordsapi.com", 1883)
client.loop_start()

def update_device_state(topic, data):
    topics_and_data[topic] = data
    message = json.dumps(data)
    client.publish(topic, message)

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

@app.route("/api/update_device", methods=["POST"])
def update_device():
    device_state = request.get_json()
    topic = f"onwords/{device_state['id']}/status"
    update_device_state(topic, device_state)
    return jsonify({"message": "Device state updated successfully!"})

if __name__ == "__main__":
    app.run(debug=True)