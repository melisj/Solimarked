#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include <SPI.h>
#include <DateTime.h>

#include "LedMatrix.h"
#include "logs.h"
#include "debugging.h"
Logger logger;

#include "settings.h"

#include "network_manager.h"
NetworkManager netmanager;

#include "processed_data.h"
Data data;


void setup() {
  Serial.begin(9600);
  setupMatrix();  

  // If connection is made, do something (optional)
  if (netmanager.startConnection()) {

  }
  if(WiFi.status() == WL_CONNECTED){
    netmanager.startDateTimeLib();
  }
  
}

void loop() {
  netmanager.doRequest(domainName + data.convertToString(), "PUT");
  debugFrame();
  delay(2000);
}
