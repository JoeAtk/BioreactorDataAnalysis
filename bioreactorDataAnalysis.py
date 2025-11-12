import paho.mqtt.client as mqtt

def main():
    broker = "engf0001.cs.ucl.ac.uk "
    port = 1883
    topic =  "bioreactor/data"
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect

    try:
        client.connect(broker, port, 60)


def on_connect(client, userdata, flags, rc, topic):
    print("Connected with result code " + str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print(f"Message received on topic {msg.topic}: {msg.payload.decode()}")


https://github.com/JoeAtk/BioreactorDataAnalysis.git