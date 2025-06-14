#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// Wi-Fi настройки
const char* ssid = "bratya-kolobki";
const char* password = "VfVfvskfhfve";

// MQTT настройки
const char* mqtt_server = "192.168.1.10";
const int mqtt_port = 1883;
const char* mqtt_user = "";               
const char* mqtt_password = "";
const char* mqtt_client_id = "actuator1";
const char* topic = "sensors/server";

// Пин для светодиода (например, D1 на ESP8266)
const int ledPin = 1;

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
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
      client.subscribe(topic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  // Парсим JSON
  StaticJsonDocument<200> doc;
  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  DeserializationError error = deserializeJson(doc, message);
  if (error) {
    Serial.println("Failed to parse JSON");
    return;
  }

  float temp = doc["value"];
  Serial.println("Received: value = " + String(temp, 1));

  // Логика управления светодиодом
  if (temp > 25.0) {
    digitalWrite(ledPin, HIGH);
    Serial.println("LED ON");
  } else {
    digitalWrite(ledPin, LOW);
    Serial.println("LED OFF");
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
