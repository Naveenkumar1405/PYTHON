import paho.mqtt.client as mqtt

broker_address = "mqtt.onwordsapi.com"
broker_port = 1883
topic = "onwords/3chfb008/currentStatus"
received_message = None  # Variable to store the received message

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe(topic)

def on_message(client, userdata, msg):
    global received_message  # Declare the variable as global to modify it
    received_message = msg.payload.decode()
    print(f"Received message: {received_message}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, broker_port)
client.loop_start()
while received_message is None:
    pass
print(f"Received message outside of the function: {received_message}")