import json
import paho.mqtt.client as mqtt

BROKER = "engf0001.cs.ucl.ac.uk"    
PORT = 1883
TOPIC = "bioreactor_sim/nofaults/telemetry/summary"

def main():
    
    topic =  "bioreactor/data"
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect

    try:
        client.connect(BROKER, PORT, keepalive=60)
    except Exception as e:
        print(f"Failed to connect to broker: {e}")
        return
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Stopping client")
        client.disconnect()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    payload_str = msg.payload.decode('utf-8')    
    # Parse the string as JSON
    data = json.loads(payload_str)
        
        # -----------------------------------------------------------------
        # YOUR ANOMALY DETECTION LOGIC STARTS HERE
        # -----------------------------------------------------------------
        
    # For now print the data
    

    
    print(f"Received data: {data['window']}")


main()  

#https://github.com/JoeAtk/BioreactorDataAnalysis.git