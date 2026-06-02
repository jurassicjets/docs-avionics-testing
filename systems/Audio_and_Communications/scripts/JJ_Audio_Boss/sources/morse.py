import numpy as np

from sources.base import AudioSource

class MorseSource(AudioSource):

    def __init__(self, freq):

        self.freq = freq
        self.phase = 0

        self.sample_rate = 48000

    def get_audio(self, frames):

        t = np.arange(frames)

        audio = 0.05 * np.sin(
            2 * np.pi *
            self.freq *
            (t + self.phase) /
            self.sample_rate
        )

        self.phase += frames

        return audio.astype(np.float32)