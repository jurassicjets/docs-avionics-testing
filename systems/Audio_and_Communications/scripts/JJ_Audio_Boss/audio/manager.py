from audio.output import create_output_stream
import sounddevice as sd


class AudioManager:

    def __init__(
            self,
            device_name,
            output_channels,
            callback):

        self.device_name = device_name
        self.output_channels = output_channels
        self.callback = callback

        self.stream = None
        self.last_error = ""

        self.device_match = (
            device_name
            .split(",")[0]
            .strip()
            .lower()
        )

    def device_exists(self):

        try:

            for dev in sd.query_devices():

                if dev["max_output_channels"] <= 0:
                    continue

                name = dev["name"].strip().lower()

                if self.device_match in name:
                    return True

        except Exception:
            pass

        return False

    def start(self):

        self.stop()

        try:

            self.stream = create_output_stream(
                self.device_name,
                self.output_channels,
                self.callback
            )

            self.stream.start()

            self.last_error = ""

            return True

        except Exception as e:

            self.stream = None
            self.last_error = str(e)

            return False

    def stop(self):

        if self.stream is None:
            return

        try:
            self.stream.stop()
        except Exception:
            pass

        try:
            self.stream.close()
        except Exception:
            pass

        self.stream = None

    def healthy(self):

        return self.stream is not None