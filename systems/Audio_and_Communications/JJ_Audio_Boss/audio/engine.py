import numpy as np


class AudioEngine:

    def __init__(self, output_channels):

        self.output_channels = output_channels

        self.sources = []

        self.callback_count = 0

        self.invalid_mappings = {}

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

        self.callback_count += 1

        outdata.fill(0)

        for source, channel_map in self.sources:

            audio = source.get_audio(frames)

            if audio.ndim == 1:

                dst_ch = channel_map[0]

                if dst_ch >= outdata.shape[1]:

                    key = f"OUT{dst_ch}"

                    if key not in self.invalid_mappings:

                        self.invalid_mappings[key] = (
                            f"Output {dst_ch} unavailable"
                        )

                    continue

                outdata[:, dst_ch] += audio

            else:

                for src_ch, dst_ch in enumerate(channel_map):

                    if src_ch >= audio.shape[1]:

                        key = f"SRC{src_ch}"

                        if key not in self.invalid_mappings:

                            self.invalid_mappings[key] = (
                                f"Source missing channel {src_ch}"
                            )

                        continue

                    if dst_ch >= outdata.shape[1]:

                        key = f"OUT{dst_ch}"

                        if key not in self.invalid_mappings:

                            self.invalid_mappings[key] = (
                                f"Output {dst_ch} unavailable"
                            )

                        continue

                    outdata[:, dst_ch] += (
                        audio[:, src_ch]
                    )