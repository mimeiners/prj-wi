//---------------------------------------------------------------------
const int sensorPinsA[] = {2, 3, 4};
const int outputPinA = 13;
bool sensorFlagsA[] = {false, false, false};
unsigned long lastActivationTimeA = 0;

const int sensorPinsB[] = {5, 6, 7};
const int outputPinB = 13;
bool sensorFlagsB[] = {false, false, false};
unsigned long lastActivationTimeB = 0;

const int sensorPinsC[] = {8, 9, 10};
const int outputPinC = 13;
bool sensorFlagsC[] = {false, false, false};
unsigned long lastActivationTimeC = 0;

const int sensorPinsD[] = {15, 16, 17};
const int outputPinD = 13;
bool sensorFlagsD[] = {false, false, false};
unsigned long lastActivationTimeD = 0;

//---------------------------------------------------------------------

void setup() {
  // Initialize the pins for the first trio
  for (int i = 0; i < 3; i++) {
    pinMode(sensorPinsA[i], INPUT);
  }
  pinMode(outputPinA, OUTPUT);
  digitalWrite(outputPinA, LOW);

  // Initialize the pins for the second trio
  for (int i = 0; i < 3; i++) {
    pinMode(sensorPinsB[i], INPUT);
  }
  pinMode(outputPinB, OUTPUT);
  digitalWrite(outputPinB, LOW);

  // Initialize the pins for the third trio
  for (int i = 0; i < 3; i++) {
    pinMode(sensorPinsC[i], INPUT);
  }
  pinMode(outputPinC, OUTPUT);
  digitalWrite(outputPinC, LOW);
  
  // Initialize the pins for the fourth trio
  for (int i = 0; i < 3; i++) {
    pinMode(sensorPinsD[i], INPUT);
  }
  pinMode(outputPinD, OUTPUT);
  digitalWrite(outputPinD, LOW);
}

//---------------------------------------------------------------------

void loop() {
  handleSensors(sensorPinsA, sensorFlagsA, outputPinA, lastActivationTimeA);
  handleSensors(sensorPinsB, sensorFlagsB, outputPinB, lastActivationTimeB);
  handleSensors(sensorPinsC, sensorFlagsC, outputPinC, lastActivationTimeC);
  handleSensors(sensorPinsD, sensorFlagsD, outputPinD, lastActivationTimeD);
}

//---------------------------------------------------------------------

void handleSensors(const int sensorPins[], bool sensorFlags[], int outputPin, unsigned long &lastActivationTime) {
  bool allSensorsActivated = true;

  for (int i = 0; i < 3; i++) {
    int sensorState = digitalRead(sensorPins[i]);

    if (sensorState == HIGH && !sensorFlags[i]) {
      sensorFlags[i] = true;
      lastActivationTime = millis();
    }

    if (sensorFlags[i] == false) {
      allSensorsActivated = false;
    }
  }

  if (allSensorsActivated && (millis() - lastActivationTime <= 50)) {
    digitalWrite(outputPin, HIGH);
  } else if (millis() - lastActivationTime > 50) {
    for (int i = 0; i < 3; i++) {
      sensorFlags[i] = false;
    }
    digitalWrite(outputPin, LOW);
  }
}

