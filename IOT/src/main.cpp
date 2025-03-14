#include "ECE140_WIFI.h"
#include "ECE140_MQTT.h"
#include <Adafruit_BMP085.h>

// MQTT client - using descriptive client ID and topic
// #define CLIENT_ID "esp32-sensors"
// #define TOPIC_PREFIX "alli/ece140/sensors"

ECE140_MQTT mqtt(CLIENT_ID, BASE_TOPIC);
ECE140_WIFI wifi;   // wifi object 

// WiFi credentials
const char* ucsdUsername = UCSD_USERNAME;
const char* ucsdPassword = "pFhaz2/j$ADPbazee3:k";
const char* wifiSsid = WIFI_SSID;
const char* nonEnterpriseWifiPassword = "sAp3rs1nLH0+spOt";

const char* clientID = CLIENT_ID;
const char* topicPrefix = BASE_TOPIC;

unsigned long lastPublish = 0; 

// void mqttCallback(char* topic, uint8_t* payload, unsigned int length){
//     Serial.print("Recieved message on topic: ");
//     Serial.println(topic); 
//     Serial.print("Message: ");
//     for(unsigned int i = 0; i < length; i++){
//         Serial.print((char)payload[i]);
//     }
//     Serial.println();
// }

Adafruit_BMP085 bmp;

void setup() {
    Serial.begin(115200);

    // Connecting to Wifi here:
    Serial.println("[Main] Connecting to Wifi...");
    wifi.connectToWPAEnterprise(wifiSsid, ucsdUsername, ucsdPassword);
    
    // *** not UCSD wifi:  ***
    // wifi.connectToWiFi(wifiSsid, nonEnterpriseWifiPassword);

    // To connect to the MQTT :
    Serial.println("Connecting to MQTT broker...");
    if (!mqtt.connectToBroker(1883)){
        Serial.println("Failed to connect to MQTT broker");
    }

    // if(mqtt.connectToBroker()){
    //     mqtt.publishMessage("status", "Sensor device connected!");
    //     Serial.println("Connected to MQTT broker");
    // }
    // else{
    //     Serial.println("Failed to connect to MQTT broker");
    // }

    // TA 6 PART 3: checking for bmp sensor
    if (!bmp.begin()) {
        Serial.println("Could not find a valid BMP180 sensor, check wiring!");
        while (1) {}
    }
}

void loop(){
    // Keep MQTT connection alive 
    mqtt.loop();

    // Read hall sensor 
    int hallValue = hallRead(); 

    // temp sensor 
    float temperature = temperatureRead();

    //temperature from bmp
    float temp_value = bmp.readTemperature();

    //pressure from bmp
    int pressure_value = bmp.readPressure();

    // String message = "{\"hall_sensor\": " + String(hallValue) + ", \"temperature\": " + String(temperature) + "}";
    String bmp_message = "{\"temperature\": " + String(temp_value) + ", \"pressure\": " + String(pressure_value) + "}";

    
    // Serial.print("Temperature = ");
    // Serial.print(temp_value);
    // Serial.println(" *C");
    
    // Serial.print("Pressure = ");
    // Serial.print(pressure_value);
    // Serial.println(" Pa");

    Serial.println("Publishing BMP Sensor Data...");
    Serial.println(bmp_message);
    mqtt.publishMessage("readings", bmp_message);
    
    delay(2000); // Waiting 2 seconds before next reading 


       // ********** LAB 6 ***********
    // Serial.println("\n== Sensor Readings ===");
    // Serial.print("Hall Sensor: ");
    // Serial.println(hallValue);
    // Serial.print("Temperature: ");
    // Serial.print(temperature);
    // Serial.println("C");
    // Serial.println("==============");
    
    // Serial.println("Publishing Sensor Data...");
    // Serial.println(message);
    // mqtt.publishMessage("readings", message);
}
    