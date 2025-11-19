import json
import threading
import paho.mqtt.client as mqtt
from queue import Queue

BROKER = "engf0001.cs.ucl.ac.uk"    
PORT = 1883
TOPIC = "bioreactor_sim/nofaults/telemetry/summary"

trainingMode = True

def main():
    
    topic =  "bioreactor/data"
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect

    try:
        client.connect(BROKER, PORT, keepalive=60)
        print("Connected to broker")
    except Exception as e:
        print(f"Failed to connect to broker: {e}")
        return
    
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Stopping client")
        client.disconnect()
    
    timer = threading.Timer(10, client.disconnect)
    timer.start()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    payload_str = msg.payload.decode('utf-8')    
    # Parse the string as JSON
    data = json.loads(payload_str)
    print(f"Received data: {data}")



def __init__(self):
    self.trainingData={
        "temperature":[],
        "ph":[],
        "rpm":[],
        "heater":[],
        "acid":[],
        "base":[]
    }


def detect(self,data):
    if trainingMode:
        self.trainingData["temperature"].append(data["temperature"])
        self.trainingData["ph"].append(data["ph"])
        self.trainingData["rpm"].append(data["rpm"])
        self.trainingData["heater"].append(data["heater"])
        self.trainingData["acid"].append(data["acid"])
        self.trainingData["base"].append(data["base"])
    

main()
#https://github.com/JoeAtk/BioreactorDataAnalysis.git