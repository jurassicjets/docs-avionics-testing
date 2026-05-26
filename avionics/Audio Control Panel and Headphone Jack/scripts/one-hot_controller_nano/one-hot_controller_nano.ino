// ================================================
//  First-Hot Logic Controller
//  Reads 8 PTT inputs (active LOW) on D2–D9
//  Outputs binary channel select on D10–D12
//  Outputs PTT overall activity on D13 (active LOW)
//  Latches control to first active input until released
// ================================================

const int NUM_CHANNELS = 8;

// Input pins D2–D9 (active LOW)
const int inputPins[NUM_CHANNELS] = {9, 8, 7, 6, 5, 4, 3, 2};

// Output pins (binary encoding of active channel)
const int outputPins[3] = {10, 11, 12};

// Global inhibit output (goes LOW if anyone PTT active)
const int inhibitPin = 13;

// Runtime state
bool inputs[NUM_CHANNELS] = {false};   // true = pressed (grounded)
bool inhibited = false;                // true = latched (someone has control)
bool inControl = false;                // true = currently held by someone
int controlIndex = -1;                 // index of current controlling channel

void setup() {
  // Setup inputs with internal pullups (active LOW)
  for (int i = 0; i < NUM_CHANNELS; i++) {
    pinMode(inputPins[i], INPUT_PULLUP);
  }

  // Setup outputs
  for (int i = 0; i < 3; i++) {
    pinMode(outputPins[i], OUTPUT);
    digitalWrite(outputPins[i], LOW);
  }

  pinMode(inhibitPin, OUTPUT);
  digitalWrite(inhibitPin, HIGH); // no one active initially

  Serial.begin(9600);
  Serial.println("First-Hot Logic Initialized");
}

void loop() {
  // --- Read inputs (active LOW) ---
  for (int i = 0; i < NUM_CHANNELS; i++) {
    inputs[i] = (digitalRead(inputPins[i]) == LOW);
  }

  // --- Determine if any are pressed ---
  bool anyPressed = false;
  for (int i = 0; i < NUM_CHANNELS; i++) {
    if (inputs[i]) {
      anyPressed = true;
      break;
    }
  }

  // --- Handle latch logic ---
  if (!inhibited) {
    // If not inhibited, find first active (lowest index wins)
    int newControl = -1;
    for (int i = 0; i < NUM_CHANNELS; i++) {
      if (inputs[i]) {
        newControl = i;
        break; // lower index = higher priority
      }
    }

    if (newControl != -1) {
      controlIndex = newControl;
      inhibited = true;
      inControl = true;
    } else {
      controlIndex = -1;
      inControl = false;
    }
  } else {
    // If currently inhibited, check if current controller released
    if (controlIndex >= 0 && !inputs[controlIndex]) {
      // Release latch
      inhibited = false;
      inControl = false;
      controlIndex = -1;
    }
  }

  // --- Output binary channel code ---
  if (inControl && controlIndex >= 0) {
    for (int bit = 0; bit < 3; bit++) {
      int bitVal = (controlIndex >> bit) & 0x01;
      digitalWrite(outputPins[bit], bitVal ? HIGH : LOW);
    }
  } else {
    // Clear outputs when no control
    for (int bit = 0; bit < 3; bit++) {
      digitalWrite(outputPins[bit], LOW);
    }
  }

  // --- Output inhibitPin (LOW = any pressed) ---
  digitalWrite(inhibitPin, anyPressed ? LOW : HIGH);

  // --- Debug info (optional) ---
  Serial.print("Inputs: ");
  for (int i = 0; i < NUM_CHANNELS; i++) {
    Serial.print(inputs[i]);
    Serial.print(" ");
  }
  Serial.print(" | Control: ");
  Serial.print(controlIndex);
  Serial.print(" | Inhib: ");
  Serial.print(inhibited);
  Serial.print(" | Any: ");
  Serial.println(anyPressed);

  delay(10); // small debounce or loop pacing
}
