import numpy as np

from sources.base import AudioSource


MORSE = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----."
}


class MorseSource(AudioSource):

    TONES = {
        "VOR": 1020,
        "NDB": 400,
        "DME": 1350
    }

    def __init__(
            self,
            identifier,
            station_type="VOR",
            volume=0.50):

        self.sample_rate = 48000

        self.station_type = station_type.upper()

        self.identifier = identifier.upper()

        self.tone_hz = self.TONES.get(
            self.station_type,
            1020
        )

        self.volume = volume

        self.signal_strength = 1.0
        self.static_amount = 0.0

        self.enabled = True

        self.position = 0

        #
        # Fade oscillator state
        #

        self.fade_phase = 0.0

        #
        # Pattern
        #

        self.pattern = self._build_pattern()

    # ------------------------------------------
    # Public API
    # ------------------------------------------

    def set_identifier(
            self,
            identifier):

        identifier = identifier.upper()

        if identifier == self.identifier:
            return

        self.identifier = identifier

        self.position = 0

        self.pattern = self._build_pattern()

    def set_signal_strength(
            self,
            strength):

        self.signal_strength = max(
            0.0,
            min(
                1.0,
                float(strength)
            )
        )

    def set_static_amount(
            self,
            amount):

        self.static_amount = max(
            0.0,
            min(
                1.0,
                float(amount)
            )
        )

    # ------------------------------------------
    # Morse Pattern Builder
    # ------------------------------------------

    def _build_pattern(self):

        unit = int(
            0.08 *
            self.sample_rate
        )

        parts = []

        phase = 0

        for letter in self.identifier:

            code = MORSE.get(letter)

            if code is None:
                continue

            for symbol in code:

                length = (
                    unit
                    if symbol == "."
                    else unit * 3
                )

                t = np.arange(length)

                tone = (
                    self.volume *
                    np.sin(
                        2 *
                        np.pi *
                        self.tone_hz *
                        (t + phase) /
                        self.sample_rate
                    )
                )

                phase += length

                parts.append(
                    tone.astype(
                        np.float32
                    )
                )

                # element gap
                parts.append(
                    np.zeros(
                        unit,
                        dtype=np.float32
                    )
                )

            # character gap
            parts.append(
                np.zeros(
                    unit * 2,
                    dtype=np.float32
                )
            )

        #
        # Repeat pause
        #

        parts.append(
            np.zeros(
                self.sample_rate * 2,
                dtype=np.float32
            )
        )

        if not parts:

            return np.zeros(
                self.sample_rate,
                dtype=np.float32
            )

        return np.concatenate(
            parts
        )

    # ------------------------------------------
    # Audio Generation
    # ------------------------------------------

    def get_audio(
            self,
            frames):

        if not self.enabled:

            return np.zeros(
                frames,
                dtype=np.float32
            )

        pattern_len = len(
            self.pattern
        )

        result = np.empty(
            frames,
            dtype=np.float32
        )

        for i in range(frames):

            result[i] = (
                self.pattern[
                    self.position
                ]
            )

            self.position += 1

            if self.position >= pattern_len:

                self.position = 0

        #
        # Continuous fading
        #

        if self.static_amount > 0:

            fade_rate = (
                0.2 +
                self.static_amount
            )

            t = (
                np.arange(frames) +
                self.fade_phase
            )

            fade = (
                1.0 -
                (
                    self.static_amount *
                    0.5
                )
                +
                (
                    self.static_amount *
                    0.5
                )
                *
                np.sin(
                    2 *
                    np.pi *
                    fade_rate *
                    t /
                    self.sample_rate
                )
            )

            result *= fade.astype(
                np.float32
            )

            self.fade_phase += frames

            #
            # Add a small amount of hiss
            #

            noise = (
                np.random.normal(
                    0,
                    1,
                    frames
                ).astype(
                    np.float32
                )
            )

            result += (
                noise *
                self.static_amount *
                0.04
            )

        #
        # Overall attenuation
        #

        result *= (
            self.signal_strength
        )

        return result