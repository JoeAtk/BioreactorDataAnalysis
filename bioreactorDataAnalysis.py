import json
import threading
import paho.mqtt.client as mqtt
from queue import Queue
import numpy as np

BROKER = "engf0001.cs.ucl.ac.uk"    
PORT = 1883
TOPIC = "bioreactor_sim/nofaults/telemetry/summary"

trainingMode = False
timeToTrain = 600  #time in seconds
z_Threshold = 3  # Z-score threshold for anomaly detection
def main():
    if trainingMode:
        TOPIC = "bioreactor_sim/nofaults/telemetry/summary" 
    else:
        # Change this to 'three_faults' or 'variable_setpoints' later
        TOPIC = "bioreactor_sim/single_fault/telemetry/summary" 
        
        #topic =  "bioreactor/data"
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect

    try:
        client.connect(BROKER, PORT, keepalive=60)
        print("Connected to broker")
    except Exception as e:
        print(f"Failed to connect to broker: {e}")
        return
    if trainingMode:
        def finalize_training():
            client.disconnect()
            print("Finalizing training...")
            detector.FinalizeTraining()
        # Add any finalization code here
        timer = threading.Timer(timeToTrain, finalize_training)
        timer.start()
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
    detector.detect(data)



class BioreactorDataDetector:
    def __init__(self):
        self.trainingData={
            "temperature":[],
            "ph":[],
            "rpm":[],
            "heater":[],
            "acid":[],
            "base":[]
        }
        self.data={
            'temperature': {"mean":29.999371449970425,"std":0.013179168279359154},
            "ph": {"mean":5.031237816106259,"std":0.13126665959872846},
            "rpm": {"mean":1000.009628822219,"std":5.096835890987153},
            "heater": {"mean":0.4627583342212756,"std":0.0030841531676136843},
            "acid": {"mean":0.0025247225904598716,"std":0.0047907077135102664},
            "base": {"mean":0.0012588990846185632,"std":0.002639881593649799}
        }
        self.tp = 0 # True Positive
        self.tn = 0 # True Negative
        self.fp = 0 # False Positive
        self.fn = 0 # False Negative

    def detect(self,data):
        if trainingMode:
            self.trainingData["temperature"].append(data["temperature_C"]['mean'])
            self.trainingData["ph"].append(data["pH"]['mean'])
            self.trainingData["rpm"].append(data["rpm"]['mean'])
            self.trainingData["heater"].append(data["actuators_avg"]["heater_pwm"])
            self.trainingData["acid"].append(data["actuators_avg"]["acid_pwm"])
            self.trainingData["base"].append(data["actuators_avg"]["base_pwm"])
            print(".", end="", flush=True)
        else:
            anomalies = []
            for key,values in data.items():
                if key in self.data:
                    mean = self.data[key]["mean"]
                    std = self.data[key]["std"]
                    z_score = (values['mean'] - mean) / std
                    if abs(z_score) > z_Threshold:
                        anomalies.append(key)
            anomaly_detected = len(anomalies) > 0
            actual_faults = len(data['faults']['last_active'])>0
            if anomaly_detected and actual_faults:
                self.tp += 1
                result = "True Positive"
            elif not anomaly_detected and not actual_faults:
                self.tn += 1
                result = "True Negative"
            elif anomaly_detected and not actual_faults:
                self.fp += 1
                result = "False Positive"
            else:
                self.fn += 1
                result = "False Negative"
            print(f"faults = {data['faults']}")
            print(f"Anomalies detected: {anomalies} | Actual faults: {data['faults']['last_active']} | Result: {result}")
            
            
    
    def FinalizeTraining(self):
        print("Training data collected:")
        for key, values in self.trainingData.items():
            mean_value = np.mean(values)
            std_dev = np.std(values)
            #in case of zero std deviation
            if std_dev == 0:
                std_dev = 0.0001
            print(f"{key} - Mean: {mean_value}, Std Dev: {std_dev}")
detector = BioreactorDataDetector()
main()
#https://github.com/JoeAtk/BioreactorDataAnalysis.git