import time


class AircraftState:

    def __init__(self):

        self.connected = False
        self.last_update = 0

        self.com1_freq = None
        self.com2_freq = None
        self.com3_freq = None

        self.nav1_freq = None
        self.nav2_freq = None

        self.adf1_freq = None
        self.adf2_freq = None

        self.dme1_distance = None
        self.dme2_distance = None

        self.marker_state = None

    def update_timestamp(self):

        self.last_update = time.time()
        self.connected = True

    def age(self):

        return time.time() - self.last_update

    def heartbeat(self):

        if self.age() > 5:
            self.connected = False

        return self.connected