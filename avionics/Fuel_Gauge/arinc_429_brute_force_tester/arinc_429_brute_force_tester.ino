/*
  ARINC 429 sweep with:
    - adaptive word spacing
    - controlled label dwell time
    - repeated transmissions per label

  Purpose:
    Better match real avionics receiver filtering behavior
*/

#define ARINC_PIN 8
#define TRIG_PIN  2

#define ARINC_HIGH PORTB |=  (1 << 0)
#define ARINC_LOW  PORTB &= ~(1 << 0)

// Fixed ARINC timing (12.5 kbps)
const uint16_t HALF_BIT_US = 40;

// Adaptive timing
uint32_t wordGapUs = 200;
const uint32_t MAX_WORD_GAP = 20000;

// Label hold control (THIS is the new key variable)
uint8_t labelHoldCount = 2;     // start small
const uint8_t MAX_LABEL_HOLD = 20;

// ---------- ARINC bit ----------
inline void rzPulse(bool bitVal)
{
    if (bitVal)
        ARINC_HIGH;
    else
        ARINC_LOW;

    delayMicroseconds(HALF_BIT_US);

    ARINC_LOW;

    delayMicroseconds(HALF_BIT_US);
}

// ---------- word generator ----------
uint32_t makeTestWord(uint8_t label)
{
    uint32_t w = 0;

    w |= label;
    w |= ((uint32_t)label << 10);
    w |= ((uint32_t)0x3 << 29);

    int ones = 0;
    for (int i = 0; i < 31; i++)
        if (w & (1UL << i)) ones++;

    if ((ones % 2) == 0)
        w |= (1UL << 31);

    return w;
}

// ---------- send word ----------
void sendWord(uint32_t w)
{
    digitalWrite(TRIG_PIN, HIGH);

    for (int i = 0; i < 32; i++)
        rzPulse((w >> i) & 1);

    digitalWrite(TRIG_PIN, LOW);

    ARINC_LOW;
    delayMicroseconds(wordGapUs);
}

// ---------- setup ----------
void setup()
{
    pinMode(ARINC_PIN, OUTPUT);
    pinMode(TRIG_PIN, OUTPUT);

    ARINC_LOW;
    digitalWrite(TRIG_PIN, LOW);

    Serial.begin(115200);
    Serial.println("ARINC label-hold sweep starting...");
}

// ---------- main loop ----------
void loop()
{
    static uint8_t label = 0;

    for (label = 0; label < 256; label++)
    {
        uint32_t word = makeTestWord(label);

        // HOLD SAME LABEL MULTIPLE TIMES
        for (uint8_t i = 0; i < labelHoldCount; i++)
        {
            sendWord(word);
        }
    }

    // --- adapt inter-word timing ---
    wordGapUs *= 2;
    if (wordGapUs > MAX_WORD_GAP)
        wordGapUs = MAX_WORD_GAP;

    // --- gradually increase label stability ---
    if (labelHoldCount < MAX_LABEL_HOLD)
        labelHoldCount++;

    Serial.print("gap(us)=");
    Serial.print(wordGapUs);
    Serial.print(" hold=");
    Serial.println(labelHoldCount);
}
