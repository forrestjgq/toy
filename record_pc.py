import asyncio
import sounddevice as sd
import sys

SAMPLE_RATE = 44100
CHANNELS = 1
BUFFER_SIZE = 1024

async def record(q: asyncio.Queue):
    def callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        # print(f"Record callback {len(indata)}")
        q.put_nowait(bytes(indata))
    
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype="int16", callback=callback, blocksize=BUFFER_SIZE):
        while True:
            await asyncio.sleep(0.01)
    print("Record exits")