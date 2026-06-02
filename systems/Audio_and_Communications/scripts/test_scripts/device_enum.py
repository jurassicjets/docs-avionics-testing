import sounddevice as sd

for i, dev in enumerate(sd.query_devices()):
    print(f"\nDevice {i}")
    print(f"Name: {dev['name']}")
    print(f"Inputs: {dev['max_input_channels']}")
    print(f"Outputs: {dev['max_output_channels']}")
    print(f"Sample Rate: {dev['default_samplerate']}")