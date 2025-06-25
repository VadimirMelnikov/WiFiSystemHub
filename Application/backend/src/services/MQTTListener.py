import paho.mqtt.client as mqtt
import os
import json
from datetime import datetime

from src.repositories.SignalRepository import SignalRepository
from src.dto.Signal import Signal


path_to_mqtt_config = os.path.join(os.path.dirname(__file__), '..', 'resources', 'mqttConfig.json')
with open(path_to_mqtt_config, 'r', encoding='utf-8') as file:
    mqtt_config = json.load(file)

path_to_mongo_config = os.path.join(os.path.dirname(__file__), '..', 'resources', 'mongoConfig.json')
with open(path_to_mongo_config, 'r', encoding='utf-8') as file:
    mongo_config = json.load(file)

sensors_repo = SignalRepository(
                                path=mongo_config['url'],
                                database=mongo_config['db'],
                                collection=mongo_config['collection'])


# Конфигурация
MQTT_CLIENT_ID = "python-listener"

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        client.subscribe(mqtt_config['topic'])
    else:
        print(f"Failed to connect to MQTT Broker with code: {rc}")


def on_message(client, userdata, msg):
    """Callback при получении сообщения"""
    if msg.topic.startswith('sensors/') and not msg.topic.endswith("server"):
        # Обработка данных от датчиков
        payload = msg.payload.decode('utf-8')
        data = json.loads(payload)
        print(f"get data: {data}")
        sensors_repo.save_signal(
            Signal(
                name=data['name'],
                group= msg.topic.split('/')[-2],
                value=data['value'],
                time_stamp=datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
            )

def main():
    # Инициализация MQTT-клиента с явным client_id
    mqtt_client = mqtt.Client(client_id=MQTT_CLIENT_ID, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    # Подключение к брокеру
    try:
        mqtt_client.reconnect_delay_set(min_delay=1, max_delay=120)
        mqtt_client.connect(mqtt_config['host'], int(mqtt_config['port']), 60)
        print(f"Connecting to MQTT Broker at {mqtt_config['host']}:{mqtt_config['port']}")
        mqtt_client.loop_forever()
    except Exception as e:
        print(f"Failed to connect to MQTT Broker: {e}")
        exit(1)
    try:
        mqtt_client.loop_forever()
    except KeyboardInterrupt:
        mqtt_client.disconnect()

if __name__ == '__main__':
    main()