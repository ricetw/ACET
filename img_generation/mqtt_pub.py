import json
import time

from paho.mqtt import client as MQTT

from configs import MQTT_IP, MQTT_PORT

topic = "ACET/ward/payload"

class ProssesMqtt():
    
    @staticmethod
    def pub2mqtt(user, ward_info):
        with open("./img_generation/json/compress_data.json") as f:
            data = json.load(f)
        image_data_str = data.get("crypto_data", "")
        str_len = 150
        i, j = 0, str_len
        data_parts = (len(image_data_str) // str_len) + 1
        
        client = MQTT.Client()
        client.connect(MQTT_IP, MQTT_PORT, 60)
        for part in range(data_parts):
            client.publish(topic, json.dumps({
                "part": part + 1,
                "total_parts": data_parts,
                "data_length": len(image_data_str[i:j]),
                "data": image_data_str[i:j]
            }))
            i = j
            j += str_len
            time.sleep(0.5)
        client.publish(f"ACET/ward/{user}", json.dumps(ward_info))
        client.disconnect()
