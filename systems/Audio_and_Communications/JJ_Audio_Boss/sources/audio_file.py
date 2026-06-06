import numpy as np
import soundfile as sf
import miniaudio

from sources.base import AudioSource


class AudioFileSource(AudioSource):

    def __init__(
            self,
            filename):

        filename = str(filename)

        if filename.lower().endswith(".wav"):

            data, samplerate = sf.read(
                filename,
                dtype="float32"
            )

        elif filename.lower().endswith(".mp3"):

            decoded = miniaudio.decode_file(
                filename,
                output_format=miniaudio.SampleFormat.FLOAT32
            )

            samplerate = decoded.sample_rate

            data = np.frombuffer(
                decoded.samples,
                dtype=np.float32
            )

            if decoded.nchannels > 1:

                data = data.reshape(
                    -1,
                    decoded.nchannels
                )

        else:

            raise ValueError(
                f"Unsupported file type: {filename}"
            )

        #
        # Require 48 kHz for now
        #

        if samplerate != 48000:

            raise ValueError(
                f"{filename} is "
                f"{samplerate} Hz "
                f"(expected 48000 Hz)"
            )

        self.data = data

        self.channels = (
            1
            if data.ndim == 1
            else data.shape[1]
        )

        self.position = 0

    def get_audio(
            self,
            frames):

        if self.channels == 1:

            result = np.empty(
                frames,
                dtype=np.float32
            )

        else:

            result = np.empty(
                (
                    frames,
                    self.channels
                ),
                dtype=np.float32
            )

        remaining = frames
        write_pos = 0

        while remaining > 0:

            available = (
                len(self.data)
                - self.position
            )

            count = min(
                remaining,
                available
            )

            result[
                write_pos:
                write_pos + count
            ] = self.data[
                self.position:
                self.position + count
            ]

            self.position += count
            write_pos += count
            remaining -= count

            if self.position >= len(
                    self.data):

                self.position = 0

        return result