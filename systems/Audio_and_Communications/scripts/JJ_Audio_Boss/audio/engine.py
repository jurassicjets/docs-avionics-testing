import numpy as np
import time

class AudioEngine:

    def __init__(self, output_channels):

        self.output_channels = output_channels

        self.sources = []

        self.callback_count = 0

    def add_source(
            self,
            source,
            channel_map):

        self.sources.append(
            (source, channel_map)
        )

    def callback(
            self,
            outdata,
            frames,
            time_info,
            status):

        now = time.time()
#        print(f"[MOTU OUT] {now:.6f} frames={frames}")

        self.callback_count += 1

        outdata.fill(0)

        for source, channel_map in self.sources:

            audio = source.get_audio(frames)

            if audio.ndim == 1:

                outdata[:, channel_map[0]] += audio

            else:

                for src_ch, dst_ch in enumerate(channel_map):

                    if src_ch < audio.shape[1]:

                        outdata[:, dst_ch] += (
                            audio[:, src_ch]
                        )