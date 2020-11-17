class Logger {

  public:
    void printError(char* message, int code) {
      Serial.printf("%s%i", message, code);
      Serial.println(" ");
    }

  public:
    void printMessage(String message) {
      Serial.println(message);
    }

    // Print error and end connection
  public:
    void returnConnectionErrorMessage(int code, char* message = "Wemos failed to connect, code: ") {
      printError(message, code);
    }
};
