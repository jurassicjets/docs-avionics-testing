/*
  ARINC429 debugger V4 — priority + wobble + staged timing

  Key properties:
    - priority label sweep ALWAYS runs first each phase
    - remainder sweep avoids duplicate priority labels
    - controlled data wobble (small triangle wave)
    - correct ARINC label bit reversal
    - phase-based dwell progression
    - LED indicates phase + activity heartbeat
*/

#define POLARITY_PIN 8
#define ENABLE_PIN   4
#define TRIG_PIN     2

// ---------- Fast IO ----------

// D8 = PB0
#define POLARITY_HIGH PORTB |=  (1 << 0)
#define POLARITY_LOW  PORTB &= ~(1 << 0)

// D4 = PD4
#define TX_ENABLE  PORTD |=  (1 << 4)
#define TX_DISABLE PORTD &= ~(1 << 4)

// D2 = PD2
#define TRIG_HIGH PORTD |=  (1 << 2)
#define TRIG_LOW  PORTD &= ~(1 << 2)

// D13 LED
#define LED_HIGH PORTB |=  (1 << 5)
#define LED_LOW  PORTB &= ~(1 << 5)

// ---------- Timing ----------

const uint16_t FULL_BIT_US = 80;
const uint16_t HALF_BIT_US = FULL_BIT_US / 2;
const uint16_t WORD_GAP_US = FULL_BIT_US * 4;

// ---------- Priority range (octal) ----------
const uint8_t PRI_START = 040;
const uint8_t PRI_END   = 0177;

// ---------- Wobble state ----------
int16_t wobble = 0;
int8_t wobbleDir = 1;

const uint16_t baseValue = 0x1234;
const int16_t wobbleMax = 6;

// ---------- LED heartbeat ----------
unsigned long lastBeat = 0;
bool beatState = false;

void heartbeat()
{
    if (millis() - lastBeat > 120)
    {
        beatState = !beatState;
        if (beatState) LED_HIGH;
        else LED_LOW;

        lastBeat = millis();
    }
}

// ---------- ARINC label reverse ----------
uint8_t reverse8(uint8_t b)
{
    b = (b & 0xF0) >> 4 | (b & 0x0F) << 4;
    b = (b & 0xCC) >> 2 | (b & 0x33) << 2;
    b = (b & 0xAA) >> 1 | (b & 0x55) << 1;
    return b;
}

// ---------- TX pulse ----------
inline void rzPulse(bool bitVal)
{
    if (bitVal)
        POLARITY_HIGH;
    else
        POLARITY_LOW;

    TX_ENABLE;

    delayMicroseconds(HALF_BIT_US);

    TX_DISABLE;

    delayMicroseconds(HALF_BIT_US);
}

// ---------- Wobbled data generator ----------
uint16_t getWobbledValue()
{
    wobble += wobbleDir;

    if (wobble >= wobbleMax) wobbleDir = -1;
    if (wobble <= -wobbleMax) wobbleDir = 1;

    return baseValue + wobble;
}

// ---------- Build ARINC word ----------
uint32_t makeTestWord(uint8_t label)
{
    uint32_t w = 0;

    // correct ARINC label ordering
    w |= reverse8(label);

    // controlled wobble data field
    uint32_t dataField = getWobbledValue();
    w |= (dataField << 10);

    // SSM = normal positive
    w |= ((uint32_t)0x0 << 29);

    // odd parity
    int ones = 0;

    for (int i = 0; i < 31; i++)
        if (w & (1UL << i)) ones++;

    if ((ones % 2) == 0)
        w |= (1UL << 31);

    return w;
}

// ---------- Send word ----------
void sendWord(uint32_t w)
{
    TRIG_HIGH;

    for (int i = 0; i < 32; i++)
        rzPulse((w >> i) & 1);

    TRIG_LOW;

    TX_DISABLE;

    delayMicroseconds(WORD_GAP_US);
}

// ---------- Hold label for time ----------
void holdLabel(uint8_t label, uint32_t ms)
{
    uint32_t word = makeTestWord(label);

    unsigned long start = millis();

    while (millis() - start < ms)
    {
        sendWord(word);
        heartbeat();
    }
}

// ---------- Priority sweep ----------
void sweepPriority(uint32_t dwellMs)
{
    for (uint8_t label = PRI_START; label <= PRI_END; label++)
    {
        holdLabel(label, dwellMs);
    }
}

// ---------- Remainder sweep ----------
void sweepRemainder(uint32_t dwellMs)
{
    for (uint16_t label = 0; label <= 0377; label++)
    {
        if (label >= PRI_START && label <= PRI_END)
            continue;

        holdLabel(label, dwellMs);
    }
}

// ---------- LED phase indicator ----------
void phaseBlink(uint8_t phase)
{
    for (uint8_t i = 0; i < phase; i++)
    {
        LED_HIGH;
        delay(100);
        LED_LOW;
        delay(100);
    }

    delay(500);
}

// ---------- Phase runner ----------
void runPhase(uint8_t phase, uint32_t dwellMs)
{
    Serial.print("PHASE ");
    Serial.println(phase);

    phaseBlink(phase);

    Serial.println("PRIORITY SWEEP");
    sweepPriority(dwellMs);

    Serial.println("REMAINDER SWEEP");
    sweepRemainder(dwellMs);
}

// ---------- Setup ----------
void setup()
{
    pinMode(POLARITY_PIN, OUTPUT);
    pinMode(ENABLE_PIN, OUTPUT);
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(LED_BUILTIN, OUTPUT);

    TX_DISABLE;
    TRIG_LOW;
    LED_LOW;

    Serial.begin(115200);

    Serial.println("ARINC429 V4 priority + wobble + phased sweep");
}

// ---------- Main ----------
void loop()
{
    runPhase(1, 250);     // fast discovery
    runPhase(2, 2000);    // medium persistence
    runPhase(3, 8000);    // long dwell
}