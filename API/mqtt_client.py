import ssl
import paho.mqtt.client as mqtt

# HiveMQ Cloud connection details
MQTT_BROKER = "216a6ebe306648f2a33cd1b87b6a7129.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USERNAME = "garind"
MQTT_PASSWORD = "TestTestTest123."
TOPIC = "fireguard/alert"

# Initialize MQTT client
client = mqtt.Client()

# Secure TLS connection
client.tls_set(tls_version=ssl.PROTOCOL_TLS)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

# Connect and handle connection result
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("*** MQTT Connected successfully ***")
        else:
            print(f"!!! MQTT Connection failed with result code {rc}")

    client.on_connect = on_connect
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_start()

# Publish a message
def publish_message(message: str):
    result = client.publish(TOPIC, message)
    status = result[0]
    if status == 0:
        print(f">>> Sent `{message}` to topic `{TOPIC}`")
    else:
        print(f"!!! Failed to send message to topic {TOPIC}")
