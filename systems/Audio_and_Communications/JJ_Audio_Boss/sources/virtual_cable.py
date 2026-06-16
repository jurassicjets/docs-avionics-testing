import sounddevice as sd
import numpy as np
import queue
import time

from sources.base import AudioSource

class VirtualCableSource(AudioSource):

    def __init__(
            self,
            device_name,
            block_size=1024,
            channels=2):

        self.channels = channels
        self.block_size = block_size

        self.queue = queue.Queue(maxsize=5)

        self.stream = sd.InputStream(
            device=device_name,
            channels=channels,
            samplerate=48000,
            blocksize=block_size,
            callback=self.input_callback
        )

        self.stream.start()

    def input_callback(
            self,
            indata,
            frames,
            time_info,
            status):

        now = time.time()
#        print(f"[VB IN ] {now:.6f} frames={frames}")
    
        try:
            self.queue.put_nowait(
                indata.copy()
            )
        except queue.Full:
            try:
                self.queue.get_nowait()  # discard oldest
            except queue.Empty:
                pass

            self.queue.put_nowait(indata.copy())
    
    def get_audio(self, frames):

        try:

            data = self.queue.get_nowait()

            if len(data) == frames:

                return data

            result = np.zeros(
                (frames, self.channels),
                dtype=np.float32
            )

            copy_len = min(
                len(data),
                frames
            )

            result[:copy_len] = data[:copy_len]

            return result

        except queue.Empty:

            return np.zeros(
                (frames, self.channels),
                dtype=np.float32
            )