class NetworkManager {
  private: WiFiClientSecure client;
  public: String retrievedData;
  
    // Setup a wifi connection
  public:
    bool startConnection() {
      // Setup the wifi connection
      WiFi.begin(networkName, password);

      while (WiFi.status() != WL_CONNECTED) {
        Serial.println("connecting");
        delay(200);
      }

      // Setup an connecion for the https server
      client.setFingerprint(fingerprint);
      if (!client.connect(host, 8443)) {
        Serial.println("Connection Failed!");
        return false;
      }

      // Check the fingerprint with the hosts certificate
      if (client.verify(fingerprint, host)) {
        Serial.println("Certificate Accepted!");
      }
      else {
        return false;
      }
      
      return true;
    }

    // Setup the DateTime libary
  public:
    void startDateTimeLib() {
      // Get current time from dutch ntp server.
      DateTime.setTimeZone(1);
      DateTime.setServer("nl.pool.ntp.org");
      DateTime.begin();
      if (!DateTime.isTimeValid()) {
        Serial.println("Failed to get time from server.");
      }
    }

    // Send request to server
  public:
    void doRequest(String url, String typeRequest) {
      if (WiFi.status() == WL_CONNECTED) {

        if (!client.connect(host, 8443)) {
          Serial.println("Connection Failed!");
          return;
        }
        
        client.print(typeRequest + " " + url + " HTTP/1.1\r\n" +
                     "Host: " + host + "\r\n" +
                     "User-Agent: ESP8266\r\n" +
                     "Connection: close\r\n\r\n"
                    );

        while (client.connected()) {
          String line = client.readStringUntil('\n');
          if (line == "\r") {
            String line = client.readStringUntil('\n');
            retrievedData = line;
            Serial.println(retrievedData);
          }
        }
      }
    }
};
