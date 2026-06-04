import time


class AudioWatchdog:

    def __init__(self):

        self.reset()

    def reset(self):

        self.last_callback_count = 0
        self.last_callback_time = time.time()

    def callbacks_alive(self, current_count):

        if current_count != self.last_callback_count:

            self.last_callback_count = current_count
            self.last_callback_time = time.time()

        return (time.time() - self.last_callback_time) < 3