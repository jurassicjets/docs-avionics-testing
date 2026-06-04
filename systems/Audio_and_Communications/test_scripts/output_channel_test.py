import sounddevice as sd
import numpy as np
import time

DEVICE_NAME = "Speakers (wr4800_821d), Windows WDM-KS"

CHANNELS = 8
SR = 48000

for active_channel in range(CHANNELS):

    print(f"Testing channel {active_channel + 1}")

    samples = SR * 1

    t = np.arange(samples)

    tone = 0.2 * np.sin(
        2 * np.pi * (100+(25*active_channel)) * t / SR
    )

    audio = np.zeros(
        (samples, CHANNELS),
        dtype=np.float32
    )

    audio[:, active_channel] = tone

    sd.play(
        audio,
        samplerate=SR,
        device=DEVICE_NAME
    )

    sd.wait()

    time.sleep(0.1)

print("Done")