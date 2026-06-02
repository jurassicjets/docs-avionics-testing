import sounddevice as sd

def create_output_stream(
        device_name,
        channels,
        callback):

    return sd.OutputStream(
        device=device_name,
        samplerate=48000,
        channels=channels,
        callback=callback,
        blocksize=0
    )