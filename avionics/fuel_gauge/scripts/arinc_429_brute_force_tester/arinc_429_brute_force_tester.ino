/*
  ARINC429 generator using CD4053

  Pin layout optimized for scope probing:

    D8 = polarity select
    D4 = inhibit / TX enable
    D2 = trigger output
*/

#define POLARITY_PIN 8
#define INHIBIT_PIN  4
#define TRIG_PIN     2

// ---------- Fast direct port access ----------

// D8 = PB0
#define POLARITY_HIGH PORTB |=  (1 << 0)
#define POLARITY_LOW  PORTB &= ~(1 << 0)

// D4 = PD4
// inhibit LOW = transmit enabled
// inhibit HIGH = outputs disconnected
#define ENABLE_TX  PORTD &= ~(1 << 4)
#define DISABLE_TX PORTD |=  (1 << 4)

// D2 = PD2
#define TRIG_HIGH PORTD |=  (1 << 2)
#define TRIG_LOW  PORTD &= ~(1 << 2)

// ---------- Timing ----------

const uint16_t FULL_BIT_US = 80;
const uint16_t HALF_BIT_US = FULL_BIT_US / 2;

// Adaptive word spacing
uint32_t wordGapUs = FULL_BIT_US * 8;
const uint32_t MAX_WORD_GAP = FULL_BIT_US * 64;

// Label hold control
uint16_t labelHoldCount = 2;
const uint16_t MAX_LABEL_HOLD = 1024;

// ---------- ARINC pulse ----------

inline void rzPulse(bool bitVal)
{
    // Select polarity
    if (bitVal)
        POLARITY_HIGH;
    else
        POLARITY_LOW;

    // Enable driver
    ENABLE_TX;

    // Active half-bit
    delayMicroseconds(HALF_BIT_US);

    // Return to null
    DISABLE_TX;

    // Null half-bit
    delayMicroseconds(HALF_BIT_US);
}

// ---------- Build ARINC word ----------

uint32_t makeTestWord(uint8_t label)
{
    uint32_t w = 0;

    // label
    w |= label;

    // mirror label into data field
    w |= ((uint32_t)label << 10);

    // SSM = normal operation
    w |= ((uint32_t)0x3 << 29);

    // odd parity
    int ones = 0;

    for (int i = 0; i < 31; i++)
    {
        if (w & (1UL << i))
            ones++;
    }

    if ((ones % 2) == 0)
        w |= (1UL << 31);

    return w;
}

// ---------- Send ARINC word ----------

void sendWord(uint32_t w)
{
    TRIG_HIGH;

    for (int i = 0; i < 32; i++)
    {
        rzPulse((w >> i) & 1);
    }

    TRIG_LOW;

    DISABLE_TX;

    delayMicroseconds(wordGapUs);
}

// ---------- Setup ----------

void setup()
{
    pinMode(POLARITY_PIN, OUTPUT);
    pinMode(INHIBIT_PIN, OUTPUT);
    pinMode(TRIG_PIN, OUTPUT);

    DISABLE_TX;
    TRIG_LOW;

    Serial.begin(115200);

    Serial.println("ARINC429 CD4053 generator");
}

// ---------- Main loop ----------

void loop()
{
    static uint8_t label = 0;

    for (label = 0; label < 256; label++)
    {
        uint32_t word = makeTestWord(label);

        for (uint16_t i = 0; i < labelHoldCount; i++)
        {
            sendWord(word);
        }
    }

    // Increase label persistence
    if (labelHoldCount < MAX_LABEL_HOLD)
    {
        labelHoldCount *= 2;
    }

    Serial.print("gap(us)=");
    Serial.print(wordGapUs);

    Serial.print(" hold=");
    Serial.println(labelHoldCount);
}