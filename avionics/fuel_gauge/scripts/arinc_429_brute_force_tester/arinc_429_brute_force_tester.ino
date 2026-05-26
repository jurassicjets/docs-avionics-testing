/*
    ARINC429 Fuel Gauge Test Generator
    ----------------------------------

    Fixed parameters discovered experimentally:

        LABEL = 034 octal
        SDI   = 3
        SSM   = 3

    Payload:
        Random BCD-encoded weight data

    Output:
        12.5 kbps ARINC429
        1 second gap between messages

    Hardware:
        Nano / ATmega328P
        CD4053 dual-mux topology

    Wiring:
        D8  -> ARINC data select
        D4  -> mux zero-state select
        D13 -> trigger + onboard LED

    Timing:
        80 us bit period
        return-to-zero signaling
*/


// ============================================================
// PIN DEFINITIONS
// ============================================================

#define DATA_PIN   8
#define ZERO_PIN   4
#define TRIG_PIN   13


// Fast direct port control
#define DATA_HIGH  PORTB |=  (1 << 0)
#define DATA_LOW   PORTB &= ~(1 << 0)

#define ZERO_HIGH  PORTD |=  (1 << 4)
#define ZERO_LOW   PORTD &= ~(1 << 4)


// ============================================================
// ARINC TIMING
// ============================================================

const uint16_t FULL_BIT_US = 80;
const uint16_t HALF_BIT_US = 40;

const uint32_t MESSAGE_GAP_MS = 1000;


// ============================================================
// ARINC CONSTANTS
// ============================================================

const uint8_t LABEL = 034;   // octal
const uint8_t SDI   = 3;
const uint8_t SSM   = 3;


// ============================================================
// ENTER ZERO STATE
// ============================================================

inline void setZeroState()
{
    ZERO_HIGH;
}


// ============================================================
// DRIVE ARINC ONE
// ============================================================

inline void driveOne()
{
    ZERO_LOW;
    DATA_HIGH;
}


// ============================================================
// DRIVE ARINC ZERO
// ============================================================

inline void driveZero()
{
    ZERO_LOW;
    DATA_LOW;
}


// ============================================================
// TRANSMIT SINGLE BIT
// ============================================================

inline void sendBit(bool bitVal)
{
    if (bitVal)
        driveOne();
    else
        driveZero();

    delayMicroseconds(HALF_BIT_US);

    setZeroState();

    delayMicroseconds(HALF_BIT_US);
}


// ============================================================
// GENERATE RANDOM BCD PAYLOAD
//
// Creates 5 BCD digits:
//
// Example:
//     12345
//
// packed into ARINC bits 11-29
// ============================================================

uint32_t generateRandomBCD()
{
    uint32_t data = 0;

    for (int digit = 0; digit < 5; digit++)
    {
        uint8_t d = random(0, 10);

        data |= ((uint32_t)d << (digit * 4));
    }

    return data;
}


// ============================================================
// BUILD ARINC WORD
// ============================================================

uint32_t buildWord()
{
    uint32_t w = 0;

    // --------------------------------------------------------
    // LABEL
    // --------------------------------------------------------

    w |= LABEL;

    // --------------------------------------------------------
    // SDI (bits 9-10)
    // --------------------------------------------------------

    w |= ((uint32_t)SDI << 8);

    // --------------------------------------------------------
    // RANDOM BCD DATA
    // --------------------------------------------------------

    uint32_t data = generateRandomBCD();

    w |= (data << 10);

    // --------------------------------------------------------
    // SSM (bits 30-31)
    // --------------------------------------------------------

    w |= ((uint32_t)SSM << 29);

    // --------------------------------------------------------
    // ODD PARITY
    // --------------------------------------------------------

    int ones = 0;

    for (int i = 0; i < 31; i++)
    {
        if (w & (1UL << i))
            ones++;
    }

    // parity bit set so TOTAL count is odd
    if ((ones % 2) == 0)
        w |= (1UL << 31);

    return w;
}


// ============================================================
// SEND COMPLETE WORD
// ============================================================

void sendWord(uint32_t w)
{
    digitalWrite(TRIG_PIN, HIGH);

    for (int i = 0; i < 32; i++)
    {
        sendBit((w >> i) & 1);
    }

    digitalWrite(TRIG_PIN, LOW);

    setZeroState();
}


// ============================================================
// SETUP
// ============================================================

void setup()
{
    pinMode(DATA_PIN, OUTPUT);
    pinMode(ZERO_PIN, OUTPUT);
    pinMode(TRIG_PIN, OUTPUT);

    setZeroState();

    digitalWrite(TRIG_PIN, LOW);

    Serial.begin(115200);

    Serial.println();
    Serial.println("ARINC429 Fuel Gauge Generator");
    Serial.println("LABEL=034 SDI=3 SSM=3");
    Serial.println();
    
    randomSeed(analogRead(A0));
}


// ============================================================
// MAIN LOOP
// ============================================================

void loop()
{
    uint32_t word = buildWord();

    sendWord(word);

    // --------------------------------------------------------
    // Debug print
    // --------------------------------------------------------

    Serial.print("TX WORD: 0x");
    Serial.println(word, HEX);

    // --------------------------------------------------------
    // Visible LED pattern
    // --------------------------------------------------------

    for (int i = 0; i < 2; i++)
    {
        digitalWrite(TRIG_PIN, HIGH);
        delay(60);

        digitalWrite(TRIG_PIN, LOW);
        delay(60);
    }

    delay(MESSAGE_GAP_MS);
}
