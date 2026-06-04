import sounddevice as sd
import numpy as np

#DEVICE_NAME = "Speakers (Focusrite USB Audio), MME"
DEVICE_NAME = "Speakers (wr4800_821d), Windows WDM-KS"
SAMPLE_RATE = 48000
CHANNELS = 8

duration = 5

samples = int(duration * SAMPLE_RATE)

audio = np.zeros((samples, CHANNELS), dtype=np.float32)

freqs = [500, 600, 700, 800, 900, 1000, 1100, 1200]
#freqs = [500, 600, 700, 800, 900, 1000, 1100, 1200, 100, 200, 300, 400, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400]

t = np.arange(samples)

for ch in range(CHANNELS):
    audio[:, ch] = 0.1 * np.sin(
        2 * np.pi * freqs[ch] * t / SAMPLE_RATE
    )

sd.play(audio, samplerate=SAMPLE_RATE, device=DEVICE_NAME)
sd.wait()