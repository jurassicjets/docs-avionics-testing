import socket
import threading


class XPlaneUDP:

    def __init__(self, state):

        self.state = state

    def start(self):

        thread = threading.Thread(
            target=self.run,
            daemon=True
        )

        thread.start()

    def run(self):

        # placeholder

        pass