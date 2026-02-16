import paho.mqtt.client as mqtt
import json
import time
import random

# Configuration
BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "jci/demo/pump_p101/telemetry"

client = mqtt.Client()

def connect_mqtt():
    try:
        client.connect(BROKER, PORT, 60)
        print(f"Connected to MQTT Broker: {BROKER}")
    except Exception as e:
        print(f"Failed to connect: {e}")

def simulate_sensor():
    connect_mqtt()
    while True:
        vibration = round(random.uniform(0.02, 0.8), 3)
        
        if vibration > 0.5:
            dominant_freq = "1x RPM (Looseness)"
            status = "CRITICAL"
        elif vibration > 0.3:
            dominant_freq = "2x RPM (Misalignment)"
            status = "WARNING"
        else:
            dominant_freq = "None (Noise Floor)"
            status = "NORMAL"
            
        payload = {
            "timestamp": time.time(),
            "vibration_rms": vibration,
            "dominant_freq": dominant_freq,
            "status": status
        }
        
        client.publish(TOPIC, json.dumps(payload))
        print(f"Publishing: {payload}")
        time.sleep(2)

if __name__ == "__main__":
    simulate_sensor()
