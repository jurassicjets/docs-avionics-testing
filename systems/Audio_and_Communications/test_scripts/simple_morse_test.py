import numpy as np
import sounddevice as sd
import threading
import time

SAMPLE_RATE = 48000
DEVICE_NAME = "Out 1-24 (MOTU Pro Audio), Windows WASAPI"

# Morse channels
CHANNELS = {
    0: "SEA",
    1: "OLM",
    2: "PDX",
    3: "SFO",
    4: "LAX",
    5: "JFK",
}

MORSE = {
    'A': '.-',
    'B': '-...',
    'C': '-.-.',
    'D': '-..',
    'E': '.',
    'F': '..-.',
    'G': '--.',
    'H': '....',
    'I': '..',
    'J': '.---',
    'K': '-.-',
    'L': '.-..',
    'M': '--',
    'N': '-.',
    'O': '---',
    'P': '.--.',
    'Q': '--.-',
    'R': '.-.',
    'S': '...',
    'T': '-',
    'U': '..-',
    'V': '...-',
    'W': '.--',
    'X': '-..-',
    'Y': '-.--',
    'Z': '--..'
}


def tone(freq=1020, duration=0.1):
    t = np.arange(int(SAMPLE_RATE * duration))
    return 0.2 * np.sin(2 * np.pi * freq * t / SAMPLE_RATE)


def silence(duration):
    return np.zeros(int(SAMPLE_RATE * duration))


def morse_audio(text):
    dot = 0.08
    dash = dot * 3

    chunks = []

    for letter in text:
        code = MORSE[letter]

        for symbol in code:
            if symbol == '.':
                chunks.append(tone(duration=dot))
            else:
                chunks.append(tone(duration=dash))

            chunks.append(silence(dot))

        chunks.append(silence(dot * 2))

    chunks.append(silence(1.5))

    return np.concatenate(chunks)


class MorseChannel:
    def __init__(self, ident):
        self.audio = morse_audio(ident)
        self.position = 0

    def get_samples(self, frames):
        out = np.zeros(frames)

        remaining = frames
        idx = 0

        while remaining > 0:
            available = len(self.audio) - self.position

            copy_len = min(available, remaining)

            out[idx:idx+copy_len] = self.audio[
                self.position:self.position+copy_len
            ]

            self.position += copy_len
            idx += copy_len
            remaining -= copy_len

            if self.position >= len(self.audio):
                self.position = 0

        return out


channels = [
    MorseChannel(ident)
    for ident in CHANNELS.values()
]


def callback(outdata, frames, time_info, status):

    outdata.fill(0)

    for ch_num, source in enumerate(channels):
        outdata[:, ch_num] = source.get_samples(frames)


stream = sd.OutputStream(
    samplerate=SAMPLE_RATE,
    channels=24,
    dtype='float32',
    callback=callback,
    device=DEVICE_NAME
)

stream.start()

print("Running...")
print("Channel 1 = SEA")
print("Channel 2 = OLM")
print("Channel 3 = PDX")
print("Channel 4 = SFO")
print("Channel 5 = LAX")
print("Channel 6 = JFK")

while True:
    time.sleep(1)