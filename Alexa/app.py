import struct
import pyaudio
import pvporcupine

porcupine = None
pa = None
audio_stream = None

try:
    porcupine = pvporcupine.create(keywords=["alexa"],
                                   access_key="XDIk0kPBzASFP2gdg/Y2S4AaIxWnefKfVJ76QR26gJtl4jeWiG+c7A==")

    pa = pyaudio.PyAudio()

    audio_stream = pa.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length)

    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:
            print("Hotword Detected")
except  Exception as e:
    print(e)