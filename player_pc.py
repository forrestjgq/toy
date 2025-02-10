
import asyncio
import io
import wave
import sounddevice as sd
import numpy as np



# 音频参数
SAMPLE_RATE = 44100
CHANNELS = 1
BUFFER_SIZE = 1024


async def play(q, *args, **kwargs):
    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # 16-bit PCM
        wf.setframerate(SAMPLE_RATE)

        def callback(outdata, frames, time, status):
            if status:
                print(status)
            try:
                data = q.get_nowait()
            except asyncio.QueueEmpty:
                data = b'\x00' * frames * 2  # 播放空白音频
            outdata[:] = np.frombuffer(data, dtype=np.int16).reshape(-1, CHANNELS)

        with sd.OutputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype="int16", callback=callback, blocksize=BUFFER_SIZE):
            while True:
                await asyncio.sleep(0.01)
        print("Play exits")