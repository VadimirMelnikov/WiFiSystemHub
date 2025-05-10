#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>      // Необходимые библиотеки
#include <WiFiClient.h>
#include <ESP8266WiFiMulti.h>
#include <ArduinoJson.h>


ESP8266WiFiMulti WiFiMulti; // объект, позволяющий устанавливать соединения сразу с несколькими модулями.


///////////////////////////////////////////////////////////////////
String data;  // строка, в которую запишется ответ сервера

//Подключение
const char* ssid = "iPhone (Савелий)"; // Имя и пароль от подсети, создаваемой сервером (другой ESP-01)
const char* password = "89373786317"; 
String serverName = "http://172.20.10.14:8000";   // IP-адресс сервера

//Режимы работы, имя, кол-во датчиков 
unsigned long previousMillis = 0;
const long interval = 7000; // временной интервал между каждым запросом
int cnt = 0;
const String name = "Client_2";
const String mode = "Ispol";
int Par[5]; 
//////////////////////////////////////////////////////////////////



void setup() {
  
  delay(5000); // задержка для того, чтобы мы успели открыть монитор порта
  Serial.begin(115200);    // Открытие паралельного порта(нужен для отладки)
  Serial.println();
  Serial.print("Connecting to ");  // К кому подключаемся
  Serial.println(ssid);
  WiFi.begin(ssid, password);   // Подключение к сети, созданной сервером
  while (WiFi.status() != WL_CONNECTED) {   // Ждем, пока не подключимся к сети сервера, попытка подключения каждые полсекунды
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("Connected to WiFi");
}

void loop() {
   //while ((Data_to_Send = Serial.readStringUntil(' ')) != "") // ждем, пока пользователь не введет строку(или микроконтроллер не передаст данные для сервера)
  unsigned long currentMillis = millis();
  if(currentMillis - previousMillis >= interval) { // проверка временного интервала


    //Sensor give data
    for(int i = 0; i < sizeof(Par) / sizeof(Par[0]); i++){
      if (cnt == 100) {cnt = 0;}
      Par[i] = cnt;
      cnt = cnt + 1;
    }
    //String Data_to_Send = genJson(Par, sizeof(Par)); // строка для отправки в сервер
    String Data_to_Send = buildJson(name, mode, Par, sizeof(Par)/sizeof(Par[0]));


    if ((WiFiMulti.run() == WL_CONNECTED)) { // провека на подключение к серверу
      data = httpGETRequest(serverName+"/data?data=" + Data_to_Send);  // Ответ на посылаемые данные .
      Serial.println("data:" + data);    // Вывод ответов в паралелльный порт
      previousMillis = currentMillis;

    //Обработка полученных данных
    ////////////////////////////////////////////////////////////////////////////////

    int params[10]; // Массив для хранения значений Params (максимум 10 элементов)
    int paramsSize = parseParams(data, params); // Вызываем функцию парсинга
  
    // Выводим результат в монитор порта(можно делать и что-то другое)
    Serial.println("Extracted Params:");
    for (int i = 0; i < paramsSize; i++) {
      Serial.println(params[i] + ' ');
    }

    ///////////////////////////////////////////////////////////////////////////////
  }
    else {
      Serial.println("WiFi Disconnected");    // проверка на подключение к серверу не прошла
    }
  }
  }

String httpGETRequest(String serverName) { //Функция, принимающая в качестве аргумента URL-путь и возвращающая ответ в виде String
  WiFiClient client;
  HTTPClient http;
    
  // Your IP address with path or Domain name with URL path 
  http.begin(client, serverName);
  
  // Send HTTP POST request
  int httpResponseCode = http.GET();
  
  String payload = "--"; 
  
  if (httpResponseCode>0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    payload = http.getString();
  }
  else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  // Free resources
  http.end();

  return payload;
}


int parseParams(String jsonString, int* params) {
  // Создаем JSON-документ
  StaticJsonDocument<200> jsonDoc; // Размер документа можно изменить в зависимости от размера JSON

  // Парсим JSON-строку
  DeserializationError error = deserializeJson(jsonDoc, jsonString);
  if (error) {
    Serial.print("JSON parsing failed: ");
    Serial.println(error.c_str());
    return 0; // Если парсинг не удался, возвращаем 0
  }

  // Извлекаем массив Params
  JsonArray paramsArray = jsonDoc["Params"];
  int paramsSize = paramsArray.size();

  // Копируем значения в массив params
  for (int i = 0; i < paramsSize && i < 10; i++) { // Ограничиваем массив 10 элементами
    params[i] = paramsArray[i];
  }

  return paramsSize; // Возвращаем количество элементов в массиве
}

String buildJson(const String name, const String mode, int* params, int paramsSize) {
  // Создаем JSON-документ
  StaticJsonDocument<200> jsonDoc; // Размер документа можно изменить в зависимости от размера данных

  // Заполняем JSON-документ
  jsonDoc["name"] = name;
  jsonDoc["mode"] = mode;

  // Добавляем массив Params
  JsonArray paramsArray = jsonDoc.createNestedArray("param");
  for (int i = 0; i < paramsSize; i++) {
    paramsArray.add(params[i]);
  }

  // Сериализуем JSON-документ в строку
  String jsonString;
  serializeJson(jsonDoc, jsonString);

  return jsonString; // Возвращаем JSON-строку
}
