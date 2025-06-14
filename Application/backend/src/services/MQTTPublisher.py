import paho.mqtt.client as mqtt
import json


class MQTTPublisher:
    def __init__(self, host="localhost", port=1883, client_id="python_publisher"):
        self.host = host
        self.port = port
        self.client_id = client_id
        self.topic = "sensors/server"

        # Создание MQTT клиента
        self.client = mqtt.Client(client_id=self.client_id)

        # Установка callback-функций
        self.client.on_connect = self.on_connect
        # self.client.on_publish = self.on_publish
        self.client.on_disconnect = self.on_disconnect

        # Подключение к брокеру
        try:
            self.client.connect(self.host, self.port, keepalive=60)
        except Exception as e:
            print(f"Ошибка подключения к брокеру {self.host}: {str(e)}")


    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Успешно подключено к брокеру {self.host}")
        else:
            print(f"Ошибка подключения, код возврата: {rc}")


    # def on_publish(self, client, userdata, mid):
    #     self.logger.info(f"Сообщение с id {mid} успешно опубликовано в топик {self.topic}")


    def on_disconnect(self, client, userdata, rc):
        print(f"Отключено от брокера, код возврата: {rc}")


    def send_data(self, data):
        payload = json.dumps({
            "name": "server",
            "value": data})

        # Публикация сообщения
        result = self.client.publish(self.topic, payload, qos=1)

        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Отправлено сообщение: {payload}")
        else:
            print(f"Ошибка при отправке сообщения, код: {result.rc}")





    def disconnect(self):
        self.client.disconnect()

    def __del__(self):
        self.disconnect()
