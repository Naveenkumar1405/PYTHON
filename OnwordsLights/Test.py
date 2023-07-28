import paho.mqtt.client as mqtt
import json

broker_address = "mqtt.onwordsapi.com"
broker_port = 1883
topics_and_data = {
    "onwords/3chfb008/status": {'id': '3chfb008', 'device1': False, 'device2': True, 'device3': False},
    "onwords/3chfb009/status": {'id': '3chfb009', 'device1': False, 'device2': True, 'device3': False},
    "onwords/3chfb006/status": {'id': '3chfb006', 'device1': False, 'device2': True, 'device3': False},
    "onwords/3chfb004/status": {'id': '3chfb004', 'device1': False, 'device2': True, 'device3': False},
    "onwords/3chfb001/status": {'id': '3chfb001', 'device1': False, 'device2': True, 'device3': False},
}
client = mqtt.Client()
client.connect(broker_address, broker_port)

for topic, data in topics_and_data.items():
    message = json.dumps(data)
    client.publish(topic, message)
client.disconnect()
