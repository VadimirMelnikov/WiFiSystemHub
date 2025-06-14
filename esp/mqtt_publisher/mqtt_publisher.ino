#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Wi-Fi настройки
const char* ssid = "bratya-kolobki";      
const char* password = "VfVfvskfhfve"; 

// MQTT настройки
const char* mqtt_server = "192.168.1.10"; 
const int mqtt_port = 1883;
const char* mqtt_user = "";               
const char* mqtt_password = "";
const char* mqtt_client_id = "ESP8266_Sensor";
const char* topic = "sensors/temperature/sensor1";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  reconnect();
}

void setup_wifi() {
  delay(10);
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected, IP: " + WiFi.localIP().toString());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Connecting to MQTT broker...");
    if (client.connect(mqtt_client_id, mqtt_user, mqtt_password)) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Генерируем случайное число (имитация температуры)
  float temperature = random(200, 300) / 10.0; // 20.0–30.0
  String payload = "{\"name\":\"sensor1\",\"value\":" + String(temperature, 1) + "}";

  // Публикуем в топик
  client.publish(topic, payload.c_str());
  Serial.println("Published: " + payload);

  delay(5000); // Публикация каждые 5 секунд
}
