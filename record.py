# -*- coding: UTF-8 -*-
import audio
import time
from machine import Pin
import asyncio


def audio_cb(event):
    if event == 0:
        print('audio-play start.')
    elif event == 7:
        print('audio-play finish.')


async def record(q: asyncio.Queue):
    aud = audio.Audio(0)
    aud.setCallback(audio_cb)
    aud.set_pa(Pin.GPIO39,2)
    aud.setVolume(11)

    record = audio.Record()
    ret = record.gain(4, 12)
    print('gain ret:{}'.format(ret))
    record.stream_start(audio.Record.AMRNB, 8000, 10)

    sz = 1024 * 10
    buf = bytearray(sz)
    while True:
        await asyncio.sleep(0.5)
        retlen = record.stream_read(buf, sz)
        if retlen <= 0:
            record.stream_start(audio.Record.AMRNB, 8000, 10)
        else:
            q.put_nowait(bytes(buf[:retlen]))


    