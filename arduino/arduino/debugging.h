#define CS_PIN D2
LedMatrix ledMatrix = LedMatrix(1, CS_PIN);

// For now this will be the frame from the thermal cam
int testingData [] = {0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 25, 0, 0, 25, 0, 0,
                      0, 0, 25, 0, 0, 25, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0,
                      25, 0, 0, 0, 0, 0, 0, 25,
                      0, 25, 0, 0, 0, 0, 25, 0,
                      0, 0, 25, 25, 25, 25, 0, 0
                     };

// Show a frame of the thermal camera on the ledmatrix
void debugFrame() {
  ledMatrix.clear();

  for (int i = 0; i < sizeof(testingData) / sizeof(testingData[0]); i++) {
    // Heat threshold for now hardcoded
    if (testingData[i] > 20)
      ledMatrix.setPixel(i % 8, int(floor(i / 8)));
  }
  ledMatrix.commit();
}

// Setup the matrix and show the initial frame
void setupMatrix() {
  ledMatrix.init();
  debugFrame();
}
