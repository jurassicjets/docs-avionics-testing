import sounddevice as sd
import numpy as np
import queue

INPUT_DEVICE = "CABLE Output (VB-Audio Virtual , Windows WASAPI"
OUTPUT_DEVICE = "Out 1-24 (MOTU Pro Audio), Windows WASAPI"

SAMPLE_RATE = 48000

INPUT_CHANNELS = 2
OUTPUT_CHANNELS = 24

audio_queue = queue.Queue(maxsize=20)

def input_callback(indata, frames, time_info, status):

    if status:
        print("INPUT:", status)

    try:
        audio_queue.put_nowait(indata.copy())
    except queue.Full:
        pass

def output_callback(outdata, frames, time_info, status):

    if status:
        print("OUTPUT:", status)

    outdata.fill(0)

    try:
        data = audio_queue.get_nowait()

        count = min(len(data), frames)

        # Route Left -> MOTU Ch1
        outdata[:count, 0] = data[:count, 0]

        # Route Right -> MOTU Ch2
        outdata[:count, 1] = data[:count, 1]

    except queue.Empty:
        pass

input_stream = sd.InputStream(
    device=INPUT_DEVICE,
    channels=INPUT_CHANNELS,
    samplerate=SAMPLE_RATE,
    callback=input_callback,
    latency='high'
)

output_stream = sd.OutputStream(
    device=OUTPUT_DEVICE,
    channels=OUTPUT_CHANNELS,
    samplerate=SAMPLE_RATE,
    callback=output_callback,
    latency='high'
)

with input_stream, output_stream:

    print("Pass-through running.")
    print("Send audio to the virtual cable.")

    while True:
        sd.sleep(1000)