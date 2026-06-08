import json
import time

from audio.engine import AudioEngine
from audio.manager import AudioManager
from audio.watchdog import AudioWatchdog

from ui.console import StatusConsole

from xplane.state import AircraftState
from xplane.udp import XPlaneUDP

from sources.virtual_cable import VirtualCableSource
from sources.morse import MorseSource
from sources.audio_file import AudioFileSource

# --------------------------------------------------
# Config
# --------------------------------------------------

with open("config/channels.json", "r") as f:
    config = json.load(f)

DEVICE_NAME = config["device"]
OUTPUT_CHANNELS = config["output_channels"]
BLOCK_SIZE = config["block_size"]


# --------------------------------------------------
# State
# --------------------------------------------------

state = AircraftState()

xplane = XPlaneUDP(state)
xplane.start()

engine = AudioEngine(
    output_channels=OUTPUT_CHANNELS
)

watchdog = AudioWatchdog()

console = StatusConsole()


# --------------------------------------------------
# Sources
# --------------------------------------------------


vhf = VirtualCableSource(
    config["vhf_cable"],
)

engine.add_source(
    vhf,
    [
        config["channels"]["VHF1"],
        config["channels"]["VHF2"]
    ]
)


#nav1 = MorseSource(
#    identifier="SEA",
#    station_type="NDB"
#)
#
#engine.add_source(
#    nav1,
#    [
#        config["channels"]["VHF1"]
#    ]
#)
#
#nav1.set_signal_strength(0.2)
#nav1.set_static_amount(0.5)


#demo = AudioFileSource(
#    "sound_samples/MSP_ATIS.wav",
#)
#
#engine.add_source(
#    demo,
#    [
#        config["channels"]["VHF1"]
#    ]
#)


# --------------------------------------------------
# Audio Manager
# --------------------------------------------------

audio_manager = AudioManager(
    DEVICE_NAME,
    OUTPUT_CHANNELS,
    engine.callback,
    BLOCK_SIZE
)


# --------------------------------------------------
# Runtime Tracking
# --------------------------------------------------

last_count = 0
last_time = time.time()

last_restart = 0
restart_count = -1

RESTART_INTERVAL = 5


# --------------------------------------------------
# Main Loop
# --------------------------------------------------

while True:

    time.sleep(1)

    now = time.time()

    cb = engine.callback_count

    callback_rate = (
        cb - last_count
    ) / (
        now - last_time
    )

    last_count = cb
    last_time = now

    state.heartbeat()

    # ------------------------------------------
    # Device Missing
    # ------------------------------------------

    if not audio_manager.device_exists():

        if audio_manager.healthy():
            audio_manager.stop()

        status = "WAITING FOR OUTPUT DEVICE"

    # ------------------------------------------
    # Device Exists, No Stream
    # ------------------------------------------

    elif not audio_manager.healthy():

        status = "RECONNECTING"

        if now - last_restart > RESTART_INTERVAL:

            if audio_manager.start():

                watchdog.reset()
                restart_count += 1

            last_restart = now

    # ------------------------------------------
    # Stream Exists
    # ------------------------------------------

    else:

        callback_ok = watchdog.callbacks_alive(
            engine.callback_count
        )

        if callback_ok:

            status = "RUNNING"

        else:

            status = "AUDIO STREAM FAILED"

            audio_manager.stop()

    # ------------------------------------------
    # Console
    # ------------------------------------------

    console.draw(
        status=status,
        output_device=DEVICE_NAME,
        callback_rate=callback_rate,
        state=state,
        restart_count=restart_count,
        last_error=audio_manager.last_error,
        warnings=engine.invalid_mappings
    )
