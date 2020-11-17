class Data {
    // Arduino ID
    String ID = WiFi.macAddress();

    // Amount of people
    int amountOfPeopleInStore = 20;
    
    // Convert the data to a json string
  public:
    String convertToString() {
      String output = "/api?peopleInStore=" + String(amountOfPeopleInStore) + "&time=" + recieveTimestamp();
      output.replace(" ", "_");
      Serial.println(domainName + output);
      return output;
    }

    // This function looks up the time on the server
    // Can later be changed to a time module for the arduino.
  public:
    String recieveTimestamp() {
      return String(DateTime.now());
    }
};
