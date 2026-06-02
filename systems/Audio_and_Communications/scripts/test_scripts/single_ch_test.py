import sounddevice as sd
import numpy as np

#DEVICE_NAME = "Speakers (Focusrite USB Audio), Windows DirectSound"
DEVICE_NAME = "Out 1-24 (MOTU Pro Audio), Windows WASAPI"
SAMPLE_RATE = 48000
CHANNELS = 24

t = np.arange(SAMPLE_RATE)

tone = 0.2 * np.sin(2 * np.pi * 1000 * t / SAMPLE_RATE)

audio = np.zeros((len(tone), CHANNELS), dtype=np.float32)

audio[:, 2] = tone  # Channel 3

sd.play(audio, samplerate=SAMPLE_RATE, device=DEVICE_NAME)

sd.wait()